"""
Integration manager to coordinate all data integrations.
Central hub for managing external data sources and exports.
"""

import logging
from typing import Dict, List, Optional, Any, Callable
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import threading
import schedule
import time

from .api_client import APIClient, SalesforceIntegration, HubSpotIntegration, GoogleAnalyticsIntegration
from .database_connector import DatabaseConnector, AWSRDSConnector, BigQueryConnector
from .file_processor import FileProcessor, CloudStorageProcessor
from .real_time_data import RealTimeDataStream, MarketDataStream, IoTDataStream
from .export_manager import ExportManager, ReportGenerator, EmailReporter, ScheduledReporter

logger = logging.getLogger(__name__)

class IntegrationManager:
    """Central manager for all data integrations."""
    
    def __init__(self):
        self.api_clients = {}
        self.database_connectors = {}
        self.file_processors = {}
        self.stream_managers = {}
        self.export_manager = ExportManager()
        self.report_generator = ReportGenerator(self.export_manager)
        self.email_reporter = None
        self.scheduled_reporter = None
        self.integration_configs = {}
        
    def setup_email_reporting(self, smtp_server: str, smtp_port: int, 
                            username: str, password: str):
        """Setup email reporting capabilities."""
        self.email_reporter = EmailReporter(smtp_server, smtp_port, username, password)
        self.scheduled_reporter = ScheduledReporter(self.export_manager, self.email_reporter)
        logger.info("Email reporting configured")
    
    def register_api_integration(self, name: str, integration_type: str, **kwargs):
        """Register API integration."""
        try:
            if integration_type == 'salesforce':
                client = SalesforceIntegration(
                    kwargs['instance_url'], 
                    kwargs['access_token']
                )
            elif integration_type == 'hubspot':
                client = HubSpotIntegration(kwargs['api_key'])
            elif integration_type == 'google_analytics':
                client = GoogleAnalyticsIntegration(kwargs['access_token'])
            elif integration_type == 'generic':
                client = APIClient()
                # Register custom endpoints
                for endpoint_config in kwargs.get('endpoints', []):
                    client.register_endpoint(endpoint_config)
            else:
                raise ValueError(f"Unsupported API integration: {integration_type}")
                
            self.api_clients[name] = client
            self.integration_configs[name] = {
                'type': 'api',
                'integration_type': integration_type,
                'config': kwargs
            }
            
            logger.info(f"Registered API integration: {name} ({integration_type})")
            
        except Exception as e:
            logger.error(f"Failed to register API integration {name}: {e}")
            raise
    
    def register_database_integration(self, name: str, db_config: Dict):
        """Register database integration."""
        try:
            connector = DatabaseConnector()
            
            if db_config['type'] == 'aws_rds':
                aws_connector = AWSRDSConnector()
                aws_connector.connect_rds_postgres(
                    name,
                    db_config['endpoint'],
                    db_config['database'],
                    db_config['username'],
                    db_config['password'],
                    db_config.get('port', 5432)
                )
                connector = aws_connector
            elif db_config['type'] == 'bigquery':
                connector = BigQueryConnector(
                    db_config['project_id'],
                    db_config.get('credentials_path')
                )
            else:
                # Standard database connection
                from .database_connector import DatabaseConfig
                config = DatabaseConfig(**db_config)
                connector.add_connection(name, config)
            
            self.database_connectors[name] = connector
            self.integration_configs[name] = {
                'type': 'database',
                'config': db_config
            }
            
            logger.info(f"Registered database integration: {name}")
            
        except Exception as e:
            logger.error(f"Failed to register database integration {name}: {e}")
            raise
    
    def register_file_integration(self, name: str, processor_type: str = 'local', **kwargs):
        """Register file processing integration."""
        try:
            if processor_type == 'cloud':
                processor = CloudStorageProcessor()
                
                # Setup cloud storage clients
                if 'aws' in kwargs:
                    processor.setup_aws(**kwargs['aws'])
                if 'gcs' in kwargs:
                    processor.setup_gcs(kwargs['gcs']['credentials_path'])
                if 'azure' in kwargs:
                    processor.setup_azure(kwargs['azure']['connection_string'])
            else:
                processor = FileProcessor()
            
            self.file_processors[name] = processor
            self.integration_configs[name] = {
                'type': 'file',
                'processor_type': processor_type,
                'config': kwargs
            }
            
            logger.info(f"Registered file integration: {name} ({processor_type})")
            
        except Exception as e:
            logger.error(f"Failed to register file integration {name}: {e}")
            raise
    
    def register_stream_integration(self, name: str, stream_type: str = 'generic', **kwargs):
        """Register real-time streaming integration."""
        try:
            if stream_type == 'market_data':
                stream_manager = MarketDataStream()
            elif stream_type == 'iot':
                stream_manager = IoTDataStream()
            else:
                stream_manager = RealTimeDataStream()
            
            self.stream_managers[name] = stream_manager
            self.integration_configs[name] = {
                'type': 'stream',
                'stream_type': stream_type,
                'config': kwargs
            }
            
            logger.info(f"Registered stream integration: {name} ({stream_type})")
            
        except Exception as e:
            logger.error(f"Failed to register stream integration {name}: {e}")
            raise
    
    def fetch_data(self, integration_name: str, **kwargs) -> pd.DataFrame:
        """Fetch data from registered integration."""
        if integration_name not in self.integration_configs:
            raise ValueError(f"Integration {integration_name} not registered")
        
        config = self.integration_configs[integration_name]
        
        try:
            if config['type'] == 'api':
                return self._fetch_api_data(integration_name, **kwargs)
            elif config['type'] == 'database':
                return self._fetch_database_data(integration_name, **kwargs)
            elif config['type'] == 'file':
                return self._fetch_file_data(integration_name, **kwargs)
            elif config['type'] == 'stream':
                return self._fetch_stream_data(integration_name, **kwargs)
            else:
                raise ValueError(f"Unknown integration type: {config['type']}")
                
        except Exception as e:
            logger.error(f"Failed to fetch data from {integration_name}: {e}")
            raise
    
    def _fetch_api_data(self, integration_name: str, **kwargs) -> pd.DataFrame:
        """Fetch data from API integration."""
        client = self.api_clients[integration_name]
        config = self.integration_configs[integration_name]
        
        if config['integration_type'] == 'salesforce':
            return client.get_accounts(kwargs.get('limit', 100))
        elif config['integration_type'] == 'hubspot':
            return client.get_contacts(kwargs.get('limit', 100))
        elif config['integration_type'] == 'google_analytics':
            return client.get_page_views(
                kwargs['view_id'],
                kwargs['start_date'],
                kwargs['end_date']
            )
        else:
            # Generic API client
            endpoint_name = kwargs.get('endpoint_name')
            params = kwargs.get('params', {})
            
            if kwargs.get('paginated', False):
                data = client.fetch_paginated_data(endpoint_name, **kwargs)
            else:
                data = client.fetch_data(endpoint_name, params)
            
            return pd.DataFrame(data) if isinstance(data, list) else pd.json_normalize(data)
    
    def _fetch_database_data(self, integration_name: str, **kwargs) -> pd.DataFrame:
        """Fetch data from database integration."""
        connector = self.database_connectors[integration_name]
        query = kwargs.get('query')
        params = kwargs.get('params', {})
        
        if not query:
            raise ValueError("Query parameter required for database integration")
        
        if hasattr(connector, 'query'):  # BigQuery
            return connector.query(query)
        else:  # Standard SQL database
            return connector.execute_query(integration_name, query, params)
    
    def _fetch_file_data(self, integration_name: str, **kwargs) -> pd.DataFrame:
        """Fetch data from file integration."""
        processor = self.file_processors[integration_name]
        
        if 'file_path' in kwargs:
            return processor.read_file(kwargs['file_path'], **kwargs)
        elif 'url' in kwargs:
            return processor.read_from_url(kwargs['url'], **kwargs)
        elif 's3_bucket' in kwargs and 's3_key' in kwargs:
            return processor.read_from_s3(kwargs['s3_bucket'], kwargs['s3_key'], **kwargs)
        else:
            raise ValueError("File source not specified")
    
    def _fetch_stream_data(self, integration_name: str, **kwargs) -> pd.DataFrame:
        """Fetch data from streaming integration."""
        stream_manager = self.stream_managers[integration_name]
        stream_name = kwargs.get('stream_name')
        count = kwargs.get('count', 100)
        
        if not stream_name:
            raise ValueError("Stream name required for stream integration")
        
        return stream_manager.get_stream_dataframe(stream_name, count)
    
    def export_data(self, data: pd.DataFrame, format_type: str, output_path: str, **kwargs) -> str:
        """Export data using export manager."""
        return self.export_manager.export_data(data, format_type, output_path, **kwargs)
    
    def generate_report(self, data: Dict[str, pd.DataFrame], output_path: str, 
                       format_type: str = 'html') -> str:
        """Generate comprehensive report."""
        return self.report_generator.generate_dashboard_report(data, output_path, format_type)
    
    def schedule_report(self, name: str, data_source: Callable, schedule: str, 
                       format_type: str, recipients: List[str] = None):
        """Schedule recurring report."""
        if not self.scheduled_reporter:
            raise ValueError("Email reporting not configured")
        
        self.scheduled_reporter.schedule_report(name, data_source, schedule, format_type, recipients)
    
    def run_scheduled_reports(self):
        """Run all scheduled reports."""
        if self.scheduled_reporter:
            self.scheduled_reporter.run_scheduled_reports()
    
    def start_scheduler(self):
        """Start the report scheduler in background thread."""
        def scheduler_worker():
            schedule.every(1).hours.do(self.run_scheduled_reports)
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
        scheduler_thread.start()
        logger.info("Report scheduler started")
    
    def test_integration(self, integration_name: str) -> bool:
        """Test integration connectivity."""
        if integration_name not in self.integration_configs:
            return False
        
        config = self.integration_configs[integration_name]
        
        try:
            if config['type'] == 'database':
                connector = self.database_connectors[integration_name]
                return connector.test_connection(integration_name)
            elif config['type'] == 'api':
                # Try a simple API call
                client = self.api_clients[integration_name]
                # Implementation depends on API type
                return True
            elif config['type'] == 'file':
                # File processor is always available
                return True
            elif config['type'] == 'stream':
                # Check if stream manager is initialized
                return integration_name in self.stream_managers
            
        except Exception as e:
            logger.error(f"Integration test failed for {integration_name}: {e}")
            return False
        
        return False
    
    def get_integration_status(self) -> Dict[str, Dict]:
        """Get status of all registered integrations."""
        status = {}
        
        for name, config in self.integration_configs.items():
            status[name] = {
                'type': config['type'],
                'status': 'connected' if self.test_integration(name) else 'disconnected',
                'last_tested': datetime.now().isoformat()
            }
        
        return status
    
    def close_all_connections(self):
        """Close all integration connections."""
        for connector in self.database_connectors.values():
            if hasattr(connector, 'close_connections'):
                connector.close_connections()
        
        for stream_manager in self.stream_managers.values():
            for stream_name in list(stream_manager.running_streams):
                stream_manager.stop_stream(stream_name)
        
        logger.info("All integration connections closed")

# Example usage and configuration
def setup_sample_integrations(manager: IntegrationManager):
    """Setup sample integrations for demonstration."""
    
    # API Integration Example
    manager.register_api_integration(
        'sample_api',
        'generic',
        endpoints=[{
            'name': 'users',
            'url': 'https://jsonplaceholder.typicode.com/users',
            'method': 'GET'
        }]
    )
    
    # Database Integration Example
    manager.register_database_integration(
        'local_db',
        {
            'type': 'sqlite',
            'database': 'data/analytics.db',
            'username': '',
            'password': '',
            'host': '',
            'port': 0
        }
    )
    
    # File Integration Example
    manager.register_file_integration(
        'local_files',
        'local'
    )
    
    # Stream Integration Example
    manager.register_stream_integration(
        'sample_stream',
        'generic'
    )
    
    logger.info("Sample integrations configured")

if __name__ == "__main__":
    # Example usage
    manager = IntegrationManager()
    setup_sample_integrations(manager)
    
    # Test integrations
    status = manager.get_integration_status()
    print("Integration Status:", status)
    
    # Fetch sample data
    try:
        api_data = manager.fetch_data('sample_api', endpoint_name='users')
        print(f"API Data: {len(api_data)} records")
        
        db_data = manager.fetch_data('local_db', query='SELECT COUNT(*) as count FROM customers')
        print(f"Database Data: {db_data}")
        
    except Exception as e:
        print(f"Error: {e}")