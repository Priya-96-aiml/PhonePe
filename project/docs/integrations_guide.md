# Data Integrations Guide

## Overview

The Data Integrations module provides comprehensive capabilities for connecting to external data sources, processing various file formats, streaming real-time data, and exporting results. This guide covers all integration types and their usage.

## 🌐 API Integrations

### Supported API Types

#### Generic REST APIs
```python
from integrations.api_client import APIClient, APIEndpoint

client = APIClient()
endpoint = APIEndpoint(
    name='users',
    url='https://api.example.com/users',
    method='GET',
    auth_type='bearer'
)

client.register_endpoint(endpoint, {'token': 'your_token'})
data = client.fetch_data('users')
```

#### Pre-configured Integrations

**Salesforce CRM**
```python
from integrations.api_client import SalesforceIntegration

sf = SalesforceIntegration(
    instance_url='https://your-instance.salesforce.com',
    access_token='your_access_token'
)

accounts = sf.get_accounts(limit=100)
```

**HubSpot CRM**
```python
from integrations.api_client import HubSpotIntegration

hs = HubSpotIntegration(api_key='your_api_key')
contacts = hs.get_contacts(limit=100)
```

**Google Analytics**
```python
from integrations.api_client import GoogleAnalyticsIntegration

ga = GoogleAnalyticsIntegration(access_token='your_token')
pageviews = ga.get_page_views('view_id', '2024-01-01', '2024-01-31')
```

### Authentication Methods

- **Bearer Token**: `auth_type='bearer'`
- **API Key**: `auth_type='api_key'`
- **Basic Auth**: `auth_type='basic'`
- **No Auth**: `auth_type='none'`

## 🗄️ Database Integrations

### Supported Databases

#### PostgreSQL
```python
from integrations.database_connector import DatabaseConnector, DatabaseConfig

connector = DatabaseConnector()
config = DatabaseConfig(
    db_type='postgresql',
    host='localhost',
    port=5432,
    database='mydb',
    username='user',
    password='password'
)

connector.add_connection('postgres_db', config)
data = connector.execute_query('postgres_db', 'SELECT * FROM users')
```

#### MySQL
```python
config = DatabaseConfig(
    db_type='mysql',
    host='localhost',
    port=3306,
    database='mydb',
    username='user',
    password='password'
)
```

#### MongoDB
```python
config = DatabaseConfig(
    db_type='mongodb',
    host='localhost',
    port=27017,
    database='mydb',
    username='user',
    password='password'
)

# Query MongoDB
data = connector.execute_mongo_query('mongo_db', 'collection_name', {'status': 'active'})
```

#### Cloud Databases

**AWS RDS**
```python
from integrations.database_connector import AWSRDSConnector

aws_connector = AWSRDSConnector()
aws_connector.connect_rds_postgres(
    'aws_db',
    'mydb.cluster-xyz.us-east-1.rds.amazonaws.com',
    'database_name',
    'username',
    'password'
)
```

**Google BigQuery**
```python
from integrations.database_connector import BigQueryConnector

bq = BigQueryConnector('project-id', 'path/to/credentials.json')
data = bq.query('SELECT * FROM dataset.table LIMIT 100')
```

## 📁 File Processing

### Local File Processing

```python
from integrations.file_processor import FileProcessor

processor = FileProcessor()

# Read various formats
csv_data = processor.read_file('data.csv')
excel_data = processor.read_file('data.xlsx', sheet_name='Sheet1')
json_data = processor.read_file('data.json')
parquet_data = processor.read_file('data.parquet')

# Write files
processor.write_file(df, 'output.csv', format_type='.csv')
processor.write_file(df, 'output.xlsx', format_type='.xlsx')
```

### Cloud Storage Integration

#### AWS S3
```python
from integrations.file_processor import CloudStorageProcessor

processor = CloudStorageProcessor()
processor.setup_aws('access_key', 'secret_key', 'us-east-1')

# Read from S3
data = processor.read_from_s3('bucket-name', 'path/to/file.csv')

# Write to S3
processor.write_to_s3(df, 'bucket-name', 'output/file.csv', '.csv')
```

#### Multiple Files
```python
# Process multiple files
dataframes = processor.read_multiple_files('data/*.csv', combine=True)

# Process ZIP files
zip_data = processor.process_zip_file('archive.zip')
```

### URL-based Files
```python
# Read from URL
url_data = processor.read_from_url('https://example.com/data.csv')
```

## 📡 Real-time Data Streams

### WebSocket Streams

```python
from integrations.real_time_data import RealTimeDataStream, StreamConfig

stream_manager = RealTimeDataStream()

config = StreamConfig(
    name='price_feed',
    source_type='websocket',
    endpoint='wss://api.example.com/stream',
    update_interval=1,
    buffer_size=1000
)

def data_callback(data):
    print(f"Received: {data}")

stream_manager.register_stream(config, data_callback)
stream_manager.start_stream('price_feed')

# Get latest data
latest_data = stream_manager.get_latest_data('price_feed', 50)
df = stream_manager.get_stream_dataframe('price_feed', 100)
```

### API Polling Streams

```python
config = StreamConfig(
    name='api_poll',
    source_type='api_polling',
    endpoint='https://api.example.com/data',
    update_interval=60  # Poll every minute
)
```

### Specialized Streams

#### Market Data
```python
from integrations.real_time_data import MarketDataStream

market_stream = MarketDataStream()
market_stream.add_stock_stream('AAPL', 'your_api_key')
market_stream.add_crypto_stream('BTCUSDT')
```

#### IoT Sensors
```python
from integrations.real_time_data import IoTDataStream

iot_stream = IoTDataStream()
iot_stream.add_sensor_stream('sensor_001', 'mqtt.broker.com', 'sensors/temperature')
```

### Stream Analytics

```python
from integrations.real_time_data import StreamingAnalytics

analytics = StreamingAnalytics(stream_manager)

# Calculate moving average
avg = analytics.calculate_moving_average('price_feed', 'price', window=10)

# Detect anomalies
anomalies = analytics.detect_anomalies('price_feed', 'price', threshold=2.0)

# Generate alerts
conditions = {
    'price': {'type': 'threshold', 'min': 100, 'max': 200}
}
alerts = analytics.generate_alerts('price_feed', conditions)
```

## 📊 Export & Reporting

### Data Export

```python
from integrations.export_manager import ExportManager

export_manager = ExportManager()

# Export to various formats
export_manager.export_data(df, 'csv', 'output.csv')
export_manager.export_data(df, 'excel', 'output.xlsx')
export_manager.export_data(df, 'json', 'output.json')
export_manager.export_data(df, 'pdf', 'report.pdf', title='My Report')
export_manager.export_data(df, 'html', 'report.html', title='Dashboard')
```

### Report Generation

```python
from integrations.export_manager import ReportGenerator

report_gen = ReportGenerator(export_manager)

# Generate dashboard report
data = {
    'transactions': transactions_df,
    'customers': customers_df,
    'products': products_df
}

report_gen.generate_dashboard_report(data, 'dashboard.html', 'html')
```

### Email Reporting

```python
from integrations.export_manager import EmailReporter

email_reporter = EmailReporter(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    username='your_email@gmail.com',
    password='your_password'
)

email_reporter.send_report(
    recipients=['recipient@example.com'],
    subject='Weekly Report',
    body='<h1>Weekly Analytics Report</h1><p>Please find attached.</p>',
    attachments=['report.pdf']
)
```

### Scheduled Reports

```python
from integrations.export_manager import ScheduledReporter

scheduled_reporter = ScheduledReporter(export_manager, email_reporter)

def get_weekly_data():
    # Your data fetching logic
    return df

scheduled_reporter.schedule_report(
    name='weekly_sales',
    data_source=get_weekly_data,
    schedule='weekly',
    format_type='pdf',
    recipients=['manager@company.com']
)

# Start scheduler
scheduled_reporter.run_scheduled_reports()
```

## 🔧 Integration Manager

### Centralized Management

```python
from integrations.integration_manager import IntegrationManager

manager = IntegrationManager()

# Setup email reporting
manager.setup_email_reporting('smtp.gmail.com', 587, 'user', 'pass')

# Register integrations
manager.register_api_integration('salesforce', 'salesforce', 
                                instance_url='https://...', access_token='...')

manager.register_database_integration('postgres', {
    'type': 'postgresql',
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'username': 'user',
    'password': 'pass'
})

manager.register_file_integration('cloud_files', 'cloud',
                                 aws={'access_key': '...', 'secret_key': '...', 'region': 'us-east-1'})

manager.register_stream_integration('market_data', 'market_data')
```

### Fetch Data from Any Integration

```python
# API data
api_data = manager.fetch_data('salesforce', limit=100)

# Database data
db_data = manager.fetch_data('postgres', query='SELECT * FROM users')

# File data
file_data = manager.fetch_data('cloud_files', s3_bucket='bucket', s3_key='data.csv')

# Stream data
stream_data = manager.fetch_data('market_data', stream_name='AAPL', count=50)
```

### System Management

```python
# Test all integrations
status = manager.get_integration_status()
print(status)

# Test specific integration
is_connected = manager.test_integration('postgres')

# Schedule reports
manager.schedule_report('daily_report', get_data_func, 'daily', 'pdf', ['user@company.com'])

# Start scheduler
manager.start_scheduler()

# Close all connections
manager.close_all_connections()
```

## 🚀 Streamlit Integration Demo

Launch the interactive demo:

```bash
streamlit run src/streamlit_integration_demo.py
```

The demo provides:

- **Overview**: System status and integration health
- **API Integrations**: Register and test API connections
- **Database Integrations**: Configure database connections and run queries
- **File Processing**: Upload files and process cloud storage
- **Real-time Streams**: Configure and monitor data streams
- **Export & Reports**: Generate and schedule reports
- **Integration Manager**: System configuration and monitoring

## 📋 Best Practices

### Security
- Store credentials in environment variables
- Use connection pooling for databases
- Implement proper authentication for APIs
- Validate all input data

### Performance
- Use appropriate buffer sizes for streams
- Implement connection pooling
- Cache frequently accessed data
- Monitor memory usage

### Error Handling
- Implement retry logic for API calls
- Handle network timeouts gracefully
- Log all errors with context
- Provide meaningful error messages

### Monitoring
- Track integration health
- Monitor data quality
- Set up alerts for failures
- Log performance metrics

## 🔍 Troubleshooting

### Common Issues

**Connection Timeouts**
- Increase timeout values
- Check network connectivity
- Verify firewall settings

**Authentication Failures**
- Verify credentials
- Check token expiration
- Confirm API permissions

**Data Format Issues**
- Validate data schemas
- Handle missing columns
- Check data types

**Memory Issues**
- Reduce buffer sizes
- Process data in chunks
- Monitor memory usage

### Getting Help

1. Check integration status in the dashboard
2. Review system logs
3. Test connections individually
4. Verify configuration settings
5. Consult API documentation

## 📚 Additional Resources

- [API Client Documentation](api_client.py)
- [Database Connector Guide](database_connector.py)
- [File Processor Manual](file_processor.py)
- [Streaming Data Guide](real_time_data.py)
- [Export Manager Reference](export_manager.py)
- [Integration Manager API](integration_manager.py)

---

This comprehensive integration system provides everything needed to connect, process, and export data from multiple sources in a unified, scalable way.