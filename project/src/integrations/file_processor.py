"""
File processor for various data formats.
Supports CSV, Excel, JSON, Parquet, and cloud storage.
"""

import logging
import pandas as pd
import json
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import boto3
from google.cloud import storage as gcs
from azure.storage.blob import BlobServiceClient
import io
import zipfile
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class FileProcessor:
    """Universal file processor for various data formats and sources."""
    
    def __init__(self):
        self.supported_formats = {
            '.csv': self._read_csv,
            '.xlsx': self._read_excel,
            '.xls': self._read_excel,
            '.json': self._read_json,
            '.parquet': self._read_parquet,
            '.txt': self._read_text,
            '.tsv': self._read_tsv
        }
    
    def read_file(self, file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """Read file and return DataFrame based on file extension."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        extension = file_path.suffix.lower()
        
        if extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {extension}")
            
        try:
            return self.supported_formats[extension](file_path, **kwargs)
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            raise
    
    def _read_csv(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """Read CSV file."""
        default_kwargs = {
            'encoding': 'utf-8',
            'low_memory': False,
            'parse_dates': True,
            'infer_datetime_format': True
        }
        default_kwargs.update(kwargs)
        return pd.read_csv(file_path, **default_kwargs)
    
    def _read_excel(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """Read Excel file."""
        default_kwargs = {
            'engine': 'openpyxl' if file_path.suffix == '.xlsx' else 'xlrd'
        }
        default_kwargs.update(kwargs)
        return pd.read_excel(file_path, **default_kwargs)
    
    def _read_json(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """Read JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.json_normalize(data)
        else:
            raise ValueError("JSON must contain array or object")
    
    def _read_parquet(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """Read Parquet file."""
        return pd.read_parquet(file_path, **kwargs)
    
    def _read_text(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """Read text file as single column DataFrame."""
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return pd.DataFrame({'text': [line.strip() for line in lines]})
    
    def _read_tsv(self, file_path: Path, **kwargs) -> pd.DataFrame:
        """Read TSV file."""
        kwargs['sep'] = '\t'
        return self._read_csv(file_path, **kwargs)
    
    def read_multiple_files(self, file_pattern: str, combine: bool = True) -> Union[pd.DataFrame, List[pd.DataFrame]]:
        """Read multiple files matching pattern."""
        from glob import glob
        
        files = glob(file_pattern)
        if not files:
            raise FileNotFoundError(f"No files found matching pattern: {file_pattern}")
        
        dataframes = []
        for file_path in files:
            try:
                df = self.read_file(file_path)
                df['source_file'] = Path(file_path).name
                dataframes.append(df)
            except Exception as e:
                logger.warning(f"Failed to read {file_path}: {e}")
        
        if combine and dataframes:
            return pd.concat(dataframes, ignore_index=True)
        return dataframes
    
    def write_file(self, df: pd.DataFrame, file_path: Union[str, Path], 
                  format_type: str = None, **kwargs):
        """Write DataFrame to file."""
        file_path = Path(file_path)
        
        if format_type is None:
            format_type = file_path.suffix.lower()
        
        try:
            if format_type == '.csv':
                df.to_csv(file_path, index=False, **kwargs)
            elif format_type in ['.xlsx', '.xls']:
                df.to_excel(file_path, index=False, **kwargs)
            elif format_type == '.json':
                df.to_json(file_path, orient='records', **kwargs)
            elif format_type == '.parquet':
                df.to_parquet(file_path, **kwargs)
            else:
                raise ValueError(f"Unsupported output format: {format_type}")
                
            logger.info(f"File written successfully: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            raise

class CloudStorageProcessor(FileProcessor):
    """File processor with cloud storage support."""
    
    def __init__(self):
        super().__init__()
        self.aws_client = None
        self.gcs_client = None
        self.azure_client = None
    
    def setup_aws(self, access_key: str, secret_key: str, region: str = 'us-east-1'):
        """Setup AWS S3 client."""
        self.aws_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        logger.info("AWS S3 client configured")
    
    def setup_gcs(self, credentials_path: str):
        """Setup Google Cloud Storage client."""
        self.gcs_client = gcs.Client.from_service_account_json(credentials_path)
        logger.info("Google Cloud Storage client configured")
    
    def setup_azure(self, connection_string: str):
        """Setup Azure Blob Storage client."""
        self.azure_client = BlobServiceClient.from_connection_string(connection_string)
        logger.info("Azure Blob Storage client configured")
    
    def read_from_s3(self, bucket: str, key: str, **kwargs) -> pd.DataFrame:
        """Read file from AWS S3."""
        if not self.aws_client:
            raise ValueError("AWS client not configured")
        
        try:
            response = self.aws_client.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read()
            
            # Determine file type from key extension
            file_extension = Path(key).suffix.lower()
            
            if file_extension == '.csv':
                return pd.read_csv(io.StringIO(content.decode('utf-8')), **kwargs)
            elif file_extension in ['.xlsx', '.xls']:
                return pd.read_excel(io.BytesIO(content), **kwargs)
            elif file_extension == '.json':
                data = json.loads(content.decode('utf-8'))
                return pd.DataFrame(data) if isinstance(data, list) else pd.json_normalize(data)
            elif file_extension == '.parquet':
                return pd.read_parquet(io.BytesIO(content), **kwargs)
            else:
                raise ValueError(f"Unsupported S3 file format: {file_extension}")
                
        except Exception as e:
            logger.error(f"Failed to read from S3 {bucket}/{key}: {e}")
            raise
    
    def write_to_s3(self, df: pd.DataFrame, bucket: str, key: str, format_type: str = '.csv'):
        """Write DataFrame to AWS S3."""
        if not self.aws_client:
            raise ValueError("AWS client not configured")
        
        try:
            buffer = io.StringIO() if format_type == '.csv' else io.BytesIO()
            
            if format_type == '.csv':
                df.to_csv(buffer, index=False)
                content = buffer.getvalue().encode('utf-8')
            elif format_type == '.json':
                df.to_json(buffer, orient='records')
                content = buffer.getvalue().encode('utf-8')
            elif format_type == '.parquet':
                df.to_parquet(buffer)
                content = buffer.getvalue()
            else:
                raise ValueError(f"Unsupported S3 output format: {format_type}")
            
            self.aws_client.put_object(Bucket=bucket, Key=key, Body=content)
            logger.info(f"File uploaded to S3: s3://{bucket}/{key}")
            
        except Exception as e:
            logger.error(f"Failed to write to S3 {bucket}/{key}: {e}")
            raise
    
    def read_from_url(self, url: str, **kwargs) -> pd.DataFrame:
        """Read file from URL."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Determine file type from URL or content-type
            content_type = response.headers.get('content-type', '')
            
            if 'csv' in content_type or url.endswith('.csv'):
                return pd.read_csv(io.StringIO(response.text), **kwargs)
            elif 'json' in content_type or url.endswith('.json'):
                data = response.json()
                return pd.DataFrame(data) if isinstance(data, list) else pd.json_normalize(data)
            elif url.endswith(('.xlsx', '.xls')):
                return pd.read_excel(io.BytesIO(response.content), **kwargs)
            else:
                # Try to parse as CSV by default
                return pd.read_csv(io.StringIO(response.text), **kwargs)
                
        except Exception as e:
            logger.error(f"Failed to read from URL {url}: {e}")
            raise
    
    def process_zip_file(self, file_path: Union[str, Path]) -> Dict[str, pd.DataFrame]:
        """Process ZIP file containing multiple data files."""
        results = {}
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                for file_name in zip_file.namelist():
                    if not file_name.endswith('/'):  # Skip directories
                        try:
                            with zip_file.open(file_name) as f:
                                content = f.read()
                                
                                # Create temporary file-like object
                                file_extension = Path(file_name).suffix.lower()
                                
                                if file_extension == '.csv':
                                    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
                                elif file_extension == '.json':
                                    data = json.loads(content.decode('utf-8'))
                                    df = pd.DataFrame(data) if isinstance(data, list) else pd.json_normalize(data)
                                elif file_extension in ['.xlsx', '.xls']:
                                    df = pd.read_excel(io.BytesIO(content))
                                else:
                                    continue  # Skip unsupported formats
                                
                                results[file_name] = df
                                
                        except Exception as e:
                            logger.warning(f"Failed to process {file_name} in ZIP: {e}")
            
            logger.info(f"Processed ZIP file with {len(results)} data files")
            return results
            
        except Exception as e:
            logger.error(f"Failed to process ZIP file {file_path}: {e}")
            raise