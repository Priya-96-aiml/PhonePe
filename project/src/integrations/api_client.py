"""
API Client for external data source integrations.
Supports REST APIs, GraphQL, and webhook endpoints.
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

@dataclass
class APIEndpoint:
    """Configuration for API endpoints."""
    name: str
    url: str
    method: str = 'GET'
    headers: Dict[str, str] = None
    auth_type: str = 'none'  # none, bearer, basic, api_key
    rate_limit: int = 100  # requests per minute
    timeout: int = 30

class APIClient:
    """Generic API client for external data integrations."""
    
    def __init__(self):
        self.session = requests.Session()
        self.endpoints = {}
        self.rate_limits = {}
        
    def register_endpoint(self, endpoint: APIEndpoint, credentials: Dict[str, str] = None):
        """Register a new API endpoint with authentication."""
        self.endpoints[endpoint.name] = endpoint
        
        # Configure authentication
        if endpoint.auth_type == 'bearer' and credentials:
            endpoint.headers = endpoint.headers or {}
            endpoint.headers['Authorization'] = f"Bearer {credentials.get('token')}"
        elif endpoint.auth_type == 'api_key' and credentials:
            endpoint.headers = endpoint.headers or {}
            endpoint.headers['X-API-Key'] = credentials.get('api_key')
        elif endpoint.auth_type == 'basic' and credentials:
            self.session.auth = (credentials.get('username'), credentials.get('password'))
            
        logger.info(f"Registered API endpoint: {endpoint.name}")
    
    def fetch_data(self, endpoint_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch data from registered API endpoint."""
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint {endpoint_name} not registered")
            
        endpoint = self.endpoints[endpoint_name]
        
        try:
            response = self.session.request(
                method=endpoint.method,
                url=endpoint.url,
                headers=endpoint.headers,
                params=params,
                timeout=endpoint.timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {endpoint_name}: {e}")
            raise
    
    def fetch_paginated_data(self, endpoint_name: str, page_param: str = 'page', 
                           max_pages: int = 10) -> List[Dict[str, Any]]:
        """Fetch paginated data from API endpoint."""
        all_data = []
        page = 1
        
        while page <= max_pages:
            try:
                params = {page_param: page}
                data = self.fetch_data(endpoint_name, params)
                
                if not data or (isinstance(data, list) and len(data) == 0):
                    break
                    
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
                    
                page += 1
                
            except Exception as e:
                logger.warning(f"Failed to fetch page {page}: {e}")
                break
                
        return all_data
    
    async def fetch_data_async(self, endpoint_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Asynchronously fetch data from API endpoint."""
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint {endpoint_name} not registered")
            
        endpoint = self.endpoints[endpoint_name]
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=endpoint.method,
                    url=endpoint.url,
                    headers=endpoint.headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=endpoint.timeout)
                ) as response:
                    response.raise_for_status()
                    return await response.json()
                    
            except aiohttp.ClientError as e:
                logger.error(f"Async API request failed for {endpoint_name}: {e}")
                raise

# Pre-configured integrations for common services
class SalesforceIntegration(APIClient):
    """Salesforce CRM integration."""
    
    def __init__(self, instance_url: str, access_token: str):
        super().__init__()
        self.register_endpoint(
            APIEndpoint(
                name='accounts',
                url=f"{instance_url}/services/data/v52.0/query",
                headers={'Authorization': f'Bearer {access_token}'}
            )
        )
    
    def get_accounts(self, limit: int = 100) -> pd.DataFrame:
        """Fetch Salesforce accounts."""
        query = f"SELECT Id, Name, Industry, AnnualRevenue FROM Account LIMIT {limit}"
        params = {'q': query}
        
        data = self.fetch_data('accounts', params)
        records = data.get('records', [])
        
        return pd.DataFrame(records)

class HubSpotIntegration(APIClient):
    """HubSpot CRM integration."""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.register_endpoint(
            APIEndpoint(
                name='contacts',
                url='https://api.hubapi.com/crm/v3/objects/contacts',
                headers={'Authorization': f'Bearer {api_key}'}
            )
        )
    
    def get_contacts(self, limit: int = 100) -> pd.DataFrame:
        """Fetch HubSpot contacts."""
        params = {'limit': limit}
        data = self.fetch_data('contacts', params)
        
        results = data.get('results', [])
        return pd.DataFrame(results)

class GoogleAnalyticsIntegration(APIClient):
    """Google Analytics integration."""
    
    def __init__(self, access_token: str):
        super().__init__()
        self.register_endpoint(
            APIEndpoint(
                name='reports',
                url='https://analyticsreporting.googleapis.com/v4/reports:batchGet',
                method='POST',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
            )
        )
    
    def get_page_views(self, view_id: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch page view data from Google Analytics."""
        request_body = {
            'reportRequests': [{
                'viewId': view_id,
                'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                'metrics': [{'expression': 'ga:pageviews'}],
                'dimensions': [{'name': 'ga:pagePath'}]
            }]
        }
        
        response = self.session.post(
            self.endpoints['reports'].url,
            headers=self.endpoints['reports'].headers,
            json=request_body
        )
        
        data = response.json()
        # Process GA response format
        return self._process_ga_response(data)
    
    def _process_ga_response(self, data: Dict) -> pd.DataFrame:
        """Process Google Analytics API response."""
        reports = data.get('reports', [])
        if not reports:
            return pd.DataFrame()
            
        report = reports[0]
        rows = report.get('data', {}).get('rows', [])
        
        processed_data = []
        for row in rows:
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [{}])[0].get('values', [])
            
            processed_data.append({
                'page_path': dimensions[0] if dimensions else '',
                'page_views': int(metrics[0]) if metrics else 0
            })
        
        return pd.DataFrame(processed_data)