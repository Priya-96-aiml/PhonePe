"""
Streamlit demo application showcasing all integrations.
Interactive interface for testing and managing data integrations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import io
import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from integrations.integration_manager import IntegrationManager, setup_sample_integrations
from integrations.api_client import APIEndpoint
from integrations.database_connector import DatabaseConfig
from integrations.real_time_data import StreamConfig

# Page configuration
st.set_page_config(
    page_title="Data Integrations Dashboard",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .integration-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .status-connected {
        color: #28a745;
        font-weight: bold;
    }
    .status-disconnected {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class IntegrationDashboard:
    """Streamlit dashboard for data integrations."""
    
    def __init__(self):
        if 'integration_manager' not in st.session_state:
            st.session_state.integration_manager = IntegrationManager()
            setup_sample_integrations(st.session_state.integration_manager)
        
        self.manager = st.session_state.integration_manager
    
    def render_sidebar(self):
        """Render sidebar navigation."""
        st.sidebar.title("🔗 Data Integrations")
        
        page = st.sidebar.selectbox(
            "Select Page",
            [
                "Overview",
                "API Integrations", 
                "Database Integrations",
                "File Processing",
                "Real-time Streams",
                "Export & Reports",
                "Integration Manager"
            ]
        )
        
        # Integration status
        st.sidebar.header("Integration Status")
        status = self.manager.get_integration_status()
        
        for name, info in status.items():
            status_class = "status-connected" if info['status'] == 'connected' else "status-disconnected"
            st.sidebar.markdown(
                f"**{name}**: <span class='{status_class}'>{info['status']}</span>",
                unsafe_allow_html=True
            )
        
        return page
    
    def render_overview(self):
        """Render overview page."""
        st.markdown('<h1 class="main-header">Data Integrations Overview</h1>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        status = self.manager.get_integration_status()
        total_integrations = len(status)
        connected_integrations = sum(1 for s in status.values() if s['status'] == 'connected')
        
        with col1:
            st.metric("Total Integrations", total_integrations)
        
        with col2:
            st.metric("Connected", connected_integrations)
        
        with col3:
            st.metric("Disconnected", total_integrations - connected_integrations)
        
        with col4:
            st.metric("Success Rate", f"{(connected_integrations/total_integrations*100):.1f}%" if total_integrations > 0 else "0%")
        
        # Integration types chart
        st.subheader("Integration Types")
        
        type_counts = {}
        for info in status.values():
            type_name = info['type'].title()
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        if type_counts:
            fig = px.pie(
                values=list(type_counts.values()),
                names=list(type_counts.keys()),
                title="Distribution of Integration Types"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent activity
        st.subheader("Integration Details")
        
        for name, info in status.items():
            with st.expander(f"{name} ({info['type'].title()})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Status:** {info['status']}")
                    st.write(f"**Type:** {info['type']}")
                
                with col2:
                    st.write(f"**Last Tested:** {info['last_tested']}")
                    
                    if st.button(f"Test Connection", key=f"test_{name}"):
                        with st.spinner("Testing connection..."):
                            result = self.manager.test_integration(name)
                            if result:
                                st.success("Connection successful!")
                            else:
                                st.error("Connection failed!")
    
    def render_api_integrations(self):
        """Render API integrations page."""
        st.header("🌐 API Integrations")
        
        tab1, tab2, tab3 = st.tabs(["Manage APIs", "Test Endpoints", "Data Preview"])
        
        with tab1:
            st.subheader("Register New API Integration")
            
            with st.form("api_integration_form"):
                name = st.text_input("Integration Name")
                integration_type = st.selectbox(
                    "Integration Type",
                    ["generic", "salesforce", "hubspot", "google_analytics"]
                )
                
                if integration_type == "generic":
                    endpoint_url = st.text_input("API Endpoint URL")
                    method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
                    auth_type = st.selectbox("Authentication", ["none", "bearer", "api_key", "basic"])
                    
                    if auth_type == "bearer":
                        token = st.text_input("Bearer Token", type="password")
                    elif auth_type == "api_key":
                        api_key = st.text_input("API Key", type="password")
                    elif auth_type == "basic":
                        username = st.text_input("Username")
                        password = st.text_input("Password", type="password")
                
                elif integration_type == "salesforce":
                    instance_url = st.text_input("Salesforce Instance URL")
                    access_token = st.text_input("Access Token", type="password")
                
                elif integration_type == "hubspot":
                    api_key = st.text_input("HubSpot API Key", type="password")
                
                elif integration_type == "google_analytics":
                    access_token = st.text_input("Google Analytics Access Token", type="password")
                
                submitted = st.form_submit_button("Register Integration")
                
                if submitted and name:
                    try:
                        if integration_type == "generic":
                            endpoint = APIEndpoint(
                                name="main",
                                url=endpoint_url,
                                method=method,
                                auth_type=auth_type
                            )
                            
                            credentials = {}
                            if auth_type == "bearer":
                                credentials['token'] = token
                            elif auth_type == "api_key":
                                credentials['api_key'] = api_key
                            elif auth_type == "basic":
                                credentials['username'] = username
                                credentials['password'] = password
                            
                            self.manager.register_api_integration(
                                name, integration_type,
                                endpoints=[endpoint],
                                credentials=credentials
                            )
                        
                        elif integration_type == "salesforce":
                            self.manager.register_api_integration(
                                name, integration_type,
                                instance_url=instance_url,
                                access_token=access_token
                            )
                        
                        elif integration_type == "hubspot":
                            self.manager.register_api_integration(
                                name, integration_type,
                                api_key=api_key
                            )
                        
                        elif integration_type == "google_analytics":
                            self.manager.register_api_integration(
                                name, integration_type,
                                access_token=access_token
                            )
                        
                        st.success(f"API integration '{name}' registered successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Failed to register integration: {e}")
        
        with tab2:
            st.subheader("Test API Endpoints")
            
            api_integrations = {name: config for name, config in self.manager.integration_configs.items() 
                              if config['type'] == 'api'}
            
            if api_integrations:
                selected_api = st.selectbox("Select API Integration", list(api_integrations.keys()))
                
                if selected_api:
                    config = api_integrations[selected_api]
                    
                    if config['integration_type'] == 'generic':
                        endpoint_name = st.text_input("Endpoint Name", value="main")
                        params = st.text_area("Parameters (JSON)", value="{}")
                        
                        if st.button("Test Endpoint"):
                            try:
                                params_dict = json.loads(params) if params.strip() else {}
                                data = self.manager.fetch_data(
                                    selected_api,
                                    endpoint_name=endpoint_name,
                                    params=params_dict
                                )
                                
                                st.success(f"Retrieved {len(data)} records")
                                st.dataframe(data.head())
                                
                            except Exception as e:
                                st.error(f"API test failed: {e}")
                    
                    else:
                        # Pre-configured integrations
                        if st.button("Test Integration"):
                            try:
                                if config['integration_type'] == 'salesforce':
                                    data = self.manager.fetch_data(selected_api, limit=10)
                                elif config['integration_type'] == 'hubspot':
                                    data = self.manager.fetch_data(selected_api, limit=10)
                                elif config['integration_type'] == 'google_analytics':
                                    view_id = st.text_input("View ID")
                                    start_date = st.date_input("Start Date")
                                    end_date = st.date_input("End Date")
                                    
                                    if view_id:
                                        data = self.manager.fetch_data(
                                            selected_api,
                                            view_id=view_id,
                                            start_date=start_date.strftime('%Y-%m-%d'),
                                            end_date=end_date.strftime('%Y-%m-%d')
                                        )
                                
                                st.success(f"Retrieved {len(data)} records")
                                st.dataframe(data.head())
                                
                            except Exception as e:
                                st.error(f"Integration test failed: {e}")
            else:
                st.info("No API integrations registered yet.")
        
        with tab3:
            st.subheader("API Data Preview")
            
            if api_integrations:
                selected_api = st.selectbox("Select API for Preview", list(api_integrations.keys()))
                
                if st.button("Fetch Data Preview"):
                    try:
                        with st.spinner("Fetching data..."):
                            data = self.manager.fetch_data(selected_api)
                            
                        st.success(f"Retrieved {len(data)} records")
                        
                        # Display data info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Records", len(data))
                        with col2:
                            st.metric("Total Columns", len(data.columns))
                        
                        # Data preview
                        st.dataframe(data)
                        
                        # Download option
                        csv = data.to_csv(index=False)
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name=f"{selected_api}_data.csv",
                            mime="text/csv"
                        )
                        
                    except Exception as e:
                        st.error(f"Failed to fetch data: {e}")
    
    def render_database_integrations(self):
        """Render database integrations page."""
        st.header("🗄️ Database Integrations")
        
        tab1, tab2, tab3 = st.tabs(["Manage Databases", "Query Interface", "Data Explorer"])
        
        with tab1:
            st.subheader("Register New Database Integration")
            
            with st.form("database_integration_form"):
                name = st.text_input("Integration Name")
                db_type = st.selectbox(
                    "Database Type",
                    ["postgresql", "mysql", "sqlite", "mongodb", "bigquery", "aws_rds"]
                )
                
                if db_type in ["postgresql", "mysql"]:
                    host = st.text_input("Host")
                    port = st.number_input("Port", value=5432 if db_type == "postgresql" else 3306)
                    database = st.text_input("Database Name")
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                
                elif db_type == "sqlite":
                    database = st.text_input("Database File Path", value="data/analytics.db")
                
                elif db_type == "bigquery":
                    project_id = st.text_input("Project ID")
                    credentials_path = st.text_input("Credentials File Path")
                
                elif db_type == "aws_rds":
                    endpoint = st.text_input("RDS Endpoint")
                    database = st.text_input("Database Name")
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    port = st.number_input("Port", value=5432)
                
                submitted = st.form_submit_button("Register Database")
                
                if submitted and name:
                    try:
                        if db_type == "sqlite":
                            config = {
                                'type': db_type,
                                'database': database,
                                'username': '',
                                'password': '',
                                'host': '',
                                'port': 0
                            }
                        elif db_type == "bigquery":
                            config = {
                                'type': db_type,
                                'project_id': project_id,
                                'credentials_path': credentials_path
                            }
                        elif db_type == "aws_rds":
                            config = {
                                'type': db_type,
                                'endpoint': endpoint,
                                'database': database,
                                'username': username,
                                'password': password,
                                'port': port
                            }
                        else:
                            config = {
                                'type': db_type,
                                'host': host,
                                'port': port,
                                'database': database,
                                'username': username,
                                'password': password
                            }
                        
                        self.manager.register_database_integration(name, config)
                        st.success(f"Database integration '{name}' registered successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Failed to register database: {e}")
        
        with tab2:
            st.subheader("SQL Query Interface")
            
            db_integrations = {name: config for name, config in self.manager.integration_configs.items() 
                             if config['type'] == 'database'}
            
            if db_integrations:
                selected_db = st.selectbox("Select Database", list(db_integrations.keys()))
                
                # Sample queries
                sample_queries = {
                    "Count Records": "SELECT COUNT(*) as total_records FROM customers;",
                    "Recent Transactions": "SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT 10;",
                    "Revenue Summary": "SELECT DATE(transaction_date) as date, SUM(total_amount) as revenue FROM transactions GROUP BY DATE(transaction_date) ORDER BY date DESC LIMIT 7;",
                    "Top Customers": "SELECT customer_id, SUM(total_amount) as total_spent FROM transactions GROUP BY customer_id ORDER BY total_spent DESC LIMIT 10;"
                }
                
                query_type = st.selectbox("Sample Queries", ["Custom"] + list(sample_queries.keys()))
                
                if query_type == "Custom":
                    query = st.text_area("SQL Query", height=150)
                else:
                    query = st.text_area("SQL Query", value=sample_queries[query_type], height=150)
                
                if st.button("Execute Query"):
                    if query.strip():
                        try:
                            with st.spinner("Executing query..."):
                                data = self.manager.fetch_data(selected_db, query=query)
                            
                            st.success(f"Query executed successfully! Retrieved {len(data)} records.")
                            st.dataframe(data)
                            
                            # Download option
                            csv = data.to_csv(index=False)
                            st.download_button(
                                label="Download Results",
                                data=csv,
                                file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                            
                        except Exception as e:
                            st.error(f"Query execution failed: {e}")
                    else:
                        st.warning("Please enter a SQL query.")
            else:
                st.info("No database integrations registered yet.")
        
        with tab3:
            st.subheader("Database Explorer")
            
            if db_integrations:
                selected_db = st.selectbox("Select Database for Exploration", list(db_integrations.keys()))
                
                # Table schema exploration
                if st.button("Explore Database Schema"):
                    try:
                        # Get table list (simplified)
                        tables_query = """
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name NOT LIKE 'sqlite_%';
                        """
                        
                        tables = self.manager.fetch_data(selected_db, query=tables_query)
                        
                        if not tables.empty:
                            st.subheader("Database Tables")
                            
                            for table_name in tables['name']:
                                with st.expander(f"Table: {table_name}"):
                                    # Get table info
                                    schema_query = f"PRAGMA table_info({table_name});"
                                    schema = self.manager.fetch_data(selected_db, query=schema_query)
                                    
                                    st.write("**Schema:**")
                                    st.dataframe(schema)
                                    
                                    # Sample data
                                    sample_query = f"SELECT * FROM {table_name} LIMIT 5;"
                                    sample_data = self.manager.fetch_data(selected_db, query=sample_query)
                                    
                                    st.write("**Sample Data:**")
                                    st.dataframe(sample_data)
                        else:
                            st.info("No tables found in database.")
                            
                    except Exception as e:
                        st.error(f"Failed to explore database: {e}")
    
    def render_file_processing(self):
        """Render file processing page."""
        st.header("📁 File Processing")
        
        tab1, tab2, tab3 = st.tabs(["Upload Files", "Cloud Storage", "Batch Processing"])
        
        with tab1:
            st.subheader("File Upload and Processing")
            
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'json', 'txt'],
                help="Supported formats: CSV, Excel, JSON, Text"
            )
            
            if uploaded_file is not None:
                try:
                    # Save uploaded file temporarily
                    file_path = f"temp_{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process file
                    processor = self.manager.file_processors.get('local_files')
                    if not processor:
                        self.manager.register_file_integration('local_files', 'local')
                        processor = self.manager.file_processors['local_files']
                    
                    data = processor.read_file(file_path)
                    
                    # Display file info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Records", len(data))
                    with col2:
                        st.metric("Columns", len(data.columns))
                    with col3:
                        st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
                    
                    # Data preview
                    st.subheader("Data Preview")
                    st.dataframe(data.head(20))
                    
                    # Data summary
                    st.subheader("Data Summary")
                    
                    # Column info
                    col_info = pd.DataFrame({
                        'Column': data.columns,
                        'Type': [str(dtype) for dtype in data.dtypes],
                        'Non-Null Count': [data[col].count() for col in data.columns],
                        'Null Count': [data[col].isnull().sum() for col in data.columns]
                    })
                    st.dataframe(col_info)
                    
                    # Numeric summary
                    numeric_cols = data.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        st.subheader("Numeric Summary")
                        st.dataframe(data[numeric_cols].describe())
                    
                    # Export options
                    st.subheader("Export Processed Data")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        export_format = st.selectbox("Export Format", ["csv", "excel", "json"])
                    
                    with col2:
                        if st.button("Export Data"):
                            output_path = f"processed_{uploaded_file.name.split('.')[0]}.{export_format}"
                            self.manager.export_data(data, export_format, output_path)
                            
                            with open(output_path, 'rb') as f:
                                st.download_button(
                                    label=f"Download {export_format.upper()}",
                                    data=f.read(),
                                    file_name=output_path,
                                    mime=f"application/{export_format}"
                                )
                    
                    # Clean up temp file
                    os.remove(file_path)
                    
                except Exception as e:
                    st.error(f"Failed to process file: {e}")
        
        with tab2:
            st.subheader("Cloud Storage Integration")
            
            cloud_provider = st.selectbox("Cloud Provider", ["AWS S3", "Google Cloud Storage", "Azure Blob"])
            
            if cloud_provider == "AWS S3":
                with st.form("s3_config"):
                    access_key = st.text_input("Access Key", type="password")
                    secret_key = st.text_input("Secret Key", type="password")
                    region = st.text_input("Region", value="us-east-1")
                    bucket = st.text_input("Bucket Name")
                    key = st.text_input("Object Key")
                    
                    if st.form_submit_button("Read from S3"):
                        try:
                            # Setup cloud processor
                            self.manager.register_file_integration(
                                'cloud_s3',
                                'cloud',
                                aws={
                                    'access_key': access_key,
                                    'secret_key': secret_key,
                                    'region': region
                                }
                            )
                            
                            data = self.manager.fetch_data(
                                'cloud_s3',
                                s3_bucket=bucket,
                                s3_key=key
                            )
                            
                            st.success(f"Successfully read {len(data)} records from S3")
                            st.dataframe(data.head())
                            
                        except Exception as e:
                            st.error(f"Failed to read from S3: {e}")
            
            elif cloud_provider == "Google Cloud Storage":
                st.info("Google Cloud Storage integration - Configure credentials file path")
                
            elif cloud_provider == "Azure Blob":
                st.info("Azure Blob Storage integration - Configure connection string")
        
        with tab3:
            st.subheader("Batch File Processing")
            
            st.info("Upload multiple files or specify file patterns for batch processing")
            
            # File pattern input
            file_pattern = st.text_input(
                "File Pattern",
                placeholder="e.g., data/*.csv",
                help="Use glob patterns to match multiple files"
            )
            
            if st.button("Process Batch Files") and file_pattern:
                try:
                    processor = self.manager.file_processors.get('local_files')
                    if not processor:
                        self.manager.register_file_integration('local_files', 'local')
                        processor = self.manager.file_processors['local_files']
                    
                    # Process multiple files
                    combined_data = processor.read_multiple_files(file_pattern, combine=True)
                    
                    if not combined_data.empty:
                        st.success(f"Processed batch files: {len(combined_data)} total records")
                        
                        # Show source file distribution
                        if 'source_file' in combined_data.columns:
                            file_counts = combined_data['source_file'].value_counts()
                            
                            fig = px.bar(
                                x=file_counts.index,
                                y=file_counts.values,
                                title="Records per File"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        st.dataframe(combined_data.head())
                    else:
                        st.warning("No files found matching the pattern")
                        
                except Exception as e:
                    st.error(f"Batch processing failed: {e}")
    
    def render_real_time_streams(self):
        """Render real-time streaming page."""
        st.header("📡 Real-time Data Streams")
        
        tab1, tab2, tab3 = st.tabs(["Stream Management", "Live Data", "Analytics"])
        
        with tab1:
            st.subheader("Configure Data Streams")
            
            with st.form("stream_config"):
                stream_name = st.text_input("Stream Name")
                stream_type = st.selectbox("Stream Type", ["websocket", "api_polling"])
                endpoint = st.text_input("Endpoint URL")
                update_interval = st.number_input("Update Interval (seconds)", value=60, min_value=1)
                buffer_size = st.number_input("Buffer Size", value=1000, min_value=100)
                
                if st.form_submit_button("Create Stream"):
                    try:
                        # Register stream integration if not exists
                        if 'sample_stream' not in self.manager.stream_managers:
                            self.manager.register_stream_integration('sample_stream', 'generic')
                        
                        stream_manager = self.manager.stream_managers['sample_stream']
                        
                        config = StreamConfig(
                            name=stream_name,
                            source_type=stream_type,
                            endpoint=endpoint,
                            update_interval=update_interval,
                            buffer_size=buffer_size,
                            auto_start=False
                        )
                        
                        stream_manager.register_stream(config)
                        st.success(f"Stream '{stream_name}' configured successfully!")
                        
                    except Exception as e:
                        st.error(f"Failed to configure stream: {e}")
            
            # Stream status
            st.subheader("Active Streams")
            
            if 'sample_stream' in self.manager.stream_managers:
                stream_manager = self.manager.stream_managers['sample_stream']
                
                for stream_name in stream_manager.streams.keys():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        status = "🟢 Running" if stream_name in stream_manager.running_streams else "🔴 Stopped"
                        st.write(f"**{stream_name}**: {status}")
                    
                    with col2:
                        if stream_name not in stream_manager.running_streams:
                            if st.button("Start", key=f"start_{stream_name}"):
                                stream_manager.start_stream(stream_name)
                                st.rerun()
                        else:
                            if st.button("Stop", key=f"stop_{stream_name}"):
                                stream_manager.stop_stream(stream_name)
                                st.rerun()
                    
                    with col3:
                        buffer_size = stream_manager.data_buffers[stream_name].qsize()
                        st.write(f"Buffer: {buffer_size}")
        
        with tab2:
            st.subheader("Live Data Monitor")
            
            if 'sample_stream' in self.manager.stream_managers:
                stream_manager = self.manager.stream_managers['sample_stream']
                
                if stream_manager.streams:
                    selected_stream = st.selectbox("Select Stream", list(stream_manager.streams.keys()))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        refresh_interval = st.number_input("Refresh Interval (seconds)", value=5, min_value=1)
                    with col2:
                        max_records = st.number_input("Max Records to Display", value=50, min_value=10)
                    
                    # Auto-refresh placeholder
                    data_placeholder = st.empty()
                    
                    if st.button("Start Live Monitor"):
                        for i in range(60):  # Run for 5 minutes max
                            try:
                                data = stream_manager.get_stream_dataframe(selected_stream, max_records)
                                
                                with data_placeholder.container():
                                    if not data.empty:
                                        st.write(f"**Latest Data** (Updated: {datetime.now().strftime('%H:%M:%S')})")
                                        st.dataframe(data)
                                        
                                        # Simple visualization if numeric data exists
                                        numeric_cols = data.select_dtypes(include=['number']).columns
                                        if len(numeric_cols) > 0 and 'timestamp' in data.columns:
                                            fig = px.line(
                                                data, 
                                                x='timestamp', 
                                                y=numeric_cols[0],
                                                title=f"{numeric_cols[0]} Over Time"
                                            )
                                            st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        st.info("No data received yet...")
                                
                                time.sleep(refresh_interval)
                                
                            except Exception as e:
                                st.error(f"Error monitoring stream: {e}")
                                break
                else:
                    st.info("No streams configured yet.")
            else:
                st.info("No stream manager available.")
        
        with tab3:
            st.subheader("Stream Analytics")
            
            st.info("Real-time analytics capabilities:")
            st.write("• Moving averages")
            st.write("• Anomaly detection")
            st.write("• Alert generation")
            st.write("• Pattern recognition")
            
            # Placeholder for analytics implementation
            st.code("""
            # Example: Calculate moving average
            from integrations.real_time_data import StreamingAnalytics
            
            analytics = StreamingAnalytics(stream_manager)
            moving_avg = analytics.calculate_moving_average('stream_name', 'value_column', window=10)
            
            # Example: Detect anomalies
            anomalies = analytics.detect_anomalies('stream_name', 'value_column', threshold=2.0)
            
            # Example: Generate alerts
            conditions = {
                'temperature': {'type': 'threshold', 'min': 0, 'max': 100}
            }
            alerts = analytics.generate_alerts('stream_name', conditions)
            """)
    
    def render_export_reports(self):
        """Render export and reports page."""
        st.header("📊 Export & Reports")
        
        tab1, tab2, tab3 = st.tabs(["Data Export", "Report Generation", "Scheduled Reports"])
        
        with tab1:
            st.subheader("Export Data")
            
            # Data source selection
            data_source = st.selectbox(
                "Select Data Source",
                ["Sample Data", "Database Query", "API Data", "File Data"]
            )
            
            sample_data = None
            
            if data_source == "Sample Data":
                # Generate sample data for export
                sample_data = pd.DataFrame({
                    'date': pd.date_range('2024-01-01', periods=100),
                    'revenue': np.random.normal(1000, 200, 100),
                    'customers': np.random.poisson(50, 100),
                    'category': np.random.choice(['A', 'B', 'C'], 100)
                })
                
                st.write("Sample data preview:")
                st.dataframe(sample_data.head())
            
            elif data_source == "Database Query":
                db_integrations = {name: config for name, config in self.manager.integration_configs.items() 
                                 if config['type'] == 'database'}
                
                if db_integrations:
                    selected_db = st.selectbox("Select Database", list(db_integrations.keys()))
                    query = st.text_area("SQL Query", value="SELECT * FROM transactions LIMIT 100;")
                    
                    if st.button("Execute Query for Export"):
                        try:
                            sample_data = self.manager.fetch_data(selected_db, query=query)
                            st.success(f"Retrieved {len(sample_data)} records")
                            st.dataframe(sample_data.head())
                        except Exception as e:
                            st.error(f"Query failed: {e}")
                else:
                    st.info("No database integrations available.")
            
            # Export options
            if sample_data is not None:
                st.subheader("Export Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    export_format = st.selectbox(
                        "Export Format",
                        ["csv", "excel", "json", "parquet", "html", "pdf"]
                    )
                
                with col2:
                    filename = st.text_input(
                        "Filename",
                        value=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                
                # Additional options based on format
                if export_format == "excel":
                    sheet_name = st.text_input("Sheet Name", value="Data")
                elif export_format == "pdf":
                    title = st.text_input("Report Title", value="Data Export Report")
                elif export_format == "html":
                    title = st.text_input("Report Title", value="Data Analysis Report")
                
                if st.button("Export Data"):
                    try:
                        output_path = f"{filename}.{export_format}"
                        
                        kwargs = {}
                        if export_format == "pdf":
                            kwargs['title'] = title
                        elif export_format == "html":
                            kwargs['title'] = title
                        
                        self.manager.export_data(sample_data, export_format, output_path, **kwargs)
                        
                        # Provide download
                        with open(output_path, 'rb') as f:
                            st.download_button(
                                label=f"Download {export_format.upper()}",
                                data=f.read(),
                                file_name=output_path,
                                mime=f"application/{export_format}"
                            )
                        
                        st.success(f"Data exported successfully as {export_format.upper()}!")
                        
                    except Exception as e:
                        st.error(f"Export failed: {e}")
        
        with tab2:
            st.subheader("Generate Reports")
            
            report_type = st.selectbox("Report Type", ["Dashboard Report", "Custom Report"])
            
            if report_type == "Dashboard Report":
                # Generate comprehensive dashboard report
                if st.button("Generate Dashboard Report"):
                    try:
                        # Create sample data for report
                        data = {
                            'transactions': pd.DataFrame({
                                'transaction_date': pd.date_range('2024-01-01', periods=100),
                                'total_amount': np.random.normal(100, 20, 100),
                                'customer_id': np.random.randint(1, 50, 100),
                                'product_category': np.random.choice(['Electronics', 'Clothing', 'Books'], 100)
                            }),
                            'customers': pd.DataFrame({
                                'customer_id': range(1, 51),
                                'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], 50)
                            })
                        }
                        
                        output_path = f"dashboard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                        
                        self.manager.generate_report(data, output_path, 'html')
                        
                        with open(output_path, 'r', encoding='utf-8') as f:
                            st.download_button(
                                label="Download Dashboard Report",
                                data=f.read(),
                                file_name=output_path,
                                mime="text/html"
                            )
                        
                        st.success("Dashboard report generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Report generation failed: {e}")
            
            elif report_type == "Custom Report":
                st.info("Custom report builder - Configure your own report template")
                
                # Custom report configuration
                with st.form("custom_report"):
                    report_title = st.text_input("Report Title")
                    include_summary = st.checkbox("Include Summary Statistics", value=True)
                    include_charts = st.checkbox("Include Charts", value=True)
                    chart_types = st.multiselect("Chart Types", ["Bar", "Line", "Pie", "Scatter"])
                    
                    if st.form_submit_button("Generate Custom Report"):
                        st.info("Custom report generation would be implemented here")
        
        with tab3:
            st.subheader("Scheduled Reports")
            
            st.info("Configure automated report generation and delivery")
            
            with st.form("schedule_report"):
                report_name = st.text_input("Report Name")
                schedule_type = st.selectbox("Schedule", ["daily", "weekly", "monthly"])
                format_type = st.selectbox("Format", ["pdf", "html", "excel"])
                
                # Email configuration
                st.subheader("Email Delivery")
                recipients = st.text_area("Recipients (one email per line)")
                
                if st.form_submit_button("Schedule Report"):
                    if report_name and recipients:
                        try:
                            recipient_list = [email.strip() for email in recipients.split('\n') if email.strip()]
                            
                            # This would require email configuration
                            st.info(f"Report '{report_name}' would be scheduled for {schedule_type} delivery to {len(recipient_list)} recipients")
                            
                            # In a real implementation:
                            # self.manager.schedule_report(
                            #     report_name,
                            #     data_source_function,
                            #     schedule_type,
                            #     format_type,
                            #     recipient_list
                            # )
                            
                        except Exception as e:
                            st.error(f"Failed to schedule report: {e}")
                    else:
                        st.warning("Please provide report name and recipients")
            
            # Show scheduled reports (placeholder)
            st.subheader("Active Scheduled Reports")
            st.info("No scheduled reports configured yet.")
    
    def render_integration_manager(self):
        """Render integration manager page."""
        st.header("⚙️ Integration Manager")
        
        tab1, tab2, tab3 = st.tabs(["System Status", "Configuration", "Logs"])
        
        with tab1:
            st.subheader("System Status")
            
            # Overall system health
            status = self.manager.get_integration_status()
            total_integrations = len(status)
            connected_integrations = sum(1 for s in status.values() if s['status'] == 'connected')
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "System Health",
                    f"{(connected_integrations/total_integrations*100):.0f}%" if total_integrations > 0 else "0%",
                    delta=None
                )
            
            with col2:
                st.metric("Active Integrations", connected_integrations)
            
            with col3:
                st.metric("Total Integrations", total_integrations)
            
            # Integration status table
            st.subheader("Integration Status Details")
            
            status_data = []
            for name, info in status.items():
                status_data.append({
                    'Name': name,
                    'Type': info['type'].title(),
                    'Status': info['status'].title(),
                    'Last Tested': info['last_tested']
                })
            
            if status_data:
                status_df = pd.DataFrame(status_data)
                st.dataframe(status_df, use_container_width=True)
            
            # Test all integrations
            if st.button("Test All Integrations"):
                with st.spinner("Testing all integrations..."):
                    results = {}
                    for name in status.keys():
                        results[name] = self.manager.test_integration(name)
                    
                    success_count = sum(results.values())
                    st.success(f"Testing complete: {success_count}/{len(results)} integrations successful")
                    
                    for name, result in results.items():
                        status_icon = "✅" if result else "❌"
                        st.write(f"{status_icon} {name}: {'Connected' if result else 'Failed'}")
        
        with tab2:
            st.subheader("System Configuration")
            
            # Email configuration
            st.subheader("Email Reporting Setup")
            
            with st.form("email_config"):
                smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
                smtp_port = st.number_input("SMTP Port", value=587)
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Configure Email"):
                    try:
                        self.manager.setup_email_reporting(smtp_server, smtp_port, username, password)
                        st.success("Email reporting configured successfully!")
                    except Exception as e:
                        st.error(f"Email configuration failed: {e}")
            
            # System settings
            st.subheader("System Settings")
            
            with st.form("system_settings"):
                log_level = st.selectbox("Log Level", ["INFO", "DEBUG", "WARNING", "ERROR"])
                max_connections = st.number_input("Max Database Connections", value=10, min_value=1)
                timeout_seconds = st.number_input("Query Timeout (seconds)", value=30, min_value=5)
                
                if st.form_submit_button("Update Settings"):
                    st.info("System settings would be updated here")
        
        with tab3:
            st.subheader("System Logs")
            
            # Log level filter
            log_level_filter = st.selectbox("Filter by Level", ["ALL", "INFO", "WARNING", "ERROR"])
            
            # Mock log entries
            log_entries = [
                {"timestamp": "2024-01-09 10:30:15", "level": "INFO", "message": "API integration 'sample_api' registered successfully"},
                {"timestamp": "2024-01-09 10:31:22", "level": "INFO", "message": "Database connection test successful"},
                {"timestamp": "2024-01-09 10:32:45", "level": "WARNING", "message": "Stream buffer approaching capacity"},
                {"timestamp": "2024-01-09 10:33:12", "level": "ERROR", "message": "Failed to connect to external API endpoint"},
                {"timestamp": "2024-01-09 10:34:33", "level": "INFO", "message": "Report generated successfully"},
            ]
            
            # Filter logs
            if log_level_filter != "ALL":
                filtered_logs = [log for log in log_entries if log["level"] == log_level_filter]
            else:
                filtered_logs = log_entries
            
            # Display logs
            for log in filtered_logs:
                level_color = {
                    "INFO": "🔵",
                    "WARNING": "🟡", 
                    "ERROR": "🔴"
                }.get(log["level"], "⚪")
                
                st.write(f"{level_color} **{log['timestamp']}** [{log['level']}] {log['message']}")
            
            # Clear logs button
            if st.button("Clear Logs"):
                st.info("Logs would be cleared here")
    
    def run(self):
        """Run the integration dashboard."""
        # Render sidebar and get selected page
        page = self.render_sidebar()
        
        # Render selected page
        if page == "Overview":
            self.render_overview()
        elif page == "API Integrations":
            self.render_api_integrations()
        elif page == "Database Integrations":
            self.render_database_integrations()
        elif page == "File Processing":
            self.render_file_processing()
        elif page == "Real-time Streams":
            self.render_real_time_streams()
        elif page == "Export & Reports":
            self.render_export_reports()
        elif page == "Integration Manager":
            self.render_integration_manager()

def main():
    """Main function to run the integration dashboard."""
    dashboard = IntegrationDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()