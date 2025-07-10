# Technical Documentation - Business Analytics Project

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Database Design](#database-design)
3. [Module Documentation](#module-documentation)
4. [API Reference](#api-reference)
5. [Performance Optimization](#performance-optimization)
6. [Security Considerations](#security-considerations)
7. [Deployment Guide](#deployment-guide)
8. [Extension Guidelines](#extension-guidelines)

## Architecture Overview

### System Architecture

The Business Analytics project follows a modular, layered architecture:

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │
│         (Streamlit Dashboard)           │
├─────────────────────────────────────────┤
│            Business Logic               │
│        (Data Analysis Module)           │
├─────────────────────────────────────────┤
│           Data Access Layer             │
│       (Database Configuration)          │
├─────────────────────────────────────────┤
│            Data Storage                 │
│          (SQLite Database)              │
└─────────────────────────────────────────┘
```

### Design Principles

**Separation of Concerns**
- Data extraction logic separated from analysis
- Database operations isolated in configuration module
- Presentation layer independent of business logic

**Modularity**
- Each module has a single responsibility
- Loose coupling between components
- High cohesion within modules

**Scalability**
- Database-agnostic design through SQLAlchemy
- Configurable data generation for testing
- Extensible analysis framework

**Maintainability**
- Comprehensive documentation
- Unit test coverage
- Consistent coding standards

## Database Design

### Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│  Customers  │    │  Transactions   │    │  Products   │
├─────────────┤    ├─────────────────┤    ├─────────────┤
│customer_id  │◄──┤customer_id (FK) │   ┌┤product_id   │
│first_name   │    │product_id (FK)  ├──►│product_name │
│last_name    │    │transaction_date │   │category     │
│email        │    │quantity         │   │brand        │
│customer_seg │    │unit_price       │   │price        │
│city         │    │total_amount     │   │cost         │
│state        │    │discount_amount  │   │stock_qty    │
└─────────────┘    │payment_method   │   └─────────────┘
                   │sales_channel    │
                   └─────────────────┘
```

### Table Specifications

#### Customers Table
```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    registration_date DATE NOT NULL,
    customer_segment TEXT CHECK(customer_segment IN ('Premium', 'Standard', 'Basic')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes**:
- `idx_customers_segment` on `customer_segment`
- Unique constraint on `email`

#### Products Table
```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    brand TEXT,
    price DECIMAL(10, 2) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes**:
- `idx_products_category` on `category`

#### Transactions Table
```sql
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    payment_method TEXT CHECK(payment_method IN ('Credit Card', 'Debit Card', 'Cash', 'PayPal')),
    sales_channel TEXT CHECK(sales_channel IN ('Online', 'In-Store', 'Mobile App')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

**Indexes**:
- `idx_transactions_date` on `transaction_date`
- `idx_transactions_customer` on `customer_id`
- `idx_transactions_product` on `product_id`

### Database Views

#### Customer Metrics View
```sql
CREATE VIEW customer_metrics AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    c.city,
    c.state,
    COUNT(t.transaction_id) as total_transactions,
    SUM(t.total_amount) as total_spent,
    AVG(t.total_amount) as avg_order_value,
    MAX(t.transaction_date) as last_purchase_date,
    MIN(t.transaction_date) as first_purchase_date
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id;
```

#### Product Performance View
```sql
CREATE VIEW product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    p.price,
    COUNT(t.transaction_id) as total_sales,
    SUM(t.quantity) as total_quantity_sold,
    SUM(t.total_amount) as total_revenue,
    AVG(t.total_amount) as avg_sale_amount
FROM products p
LEFT JOIN transactions t ON p.product_id = t.product_id
GROUP BY p.product_id;
```

## Module Documentation

### config/database_config.py

**Purpose**: Database connection and configuration management

**Classes**:

#### DatabaseConfig
```python
class DatabaseConfig:
    def __init__(self, db_path: str = "data/analytics.db")
    def get_connection(self) -> sqlite3.Connection
    def get_engine(self) -> sqlalchemy.Engine
    def execute_query(self, query: str, params: Optional[tuple] = None) -> list
    def execute_script(self, script_path: str) -> None
```

**Key Features**:
- Singleton pattern for database connections
- SQLAlchemy integration for pandas compatibility
- Automatic directory creation
- Connection pooling and management

**Usage Example**:
```python
from config.database_config import db_config

# Execute query
results = db_config.execute_query("SELECT * FROM customers LIMIT 10")

# Get pandas-compatible engine
engine = db_config.get_engine()
df = pd.read_sql_query("SELECT * FROM transactions", engine)
```

### src/data_extraction.py

**Purpose**: Data loading, validation, and preprocessing

**Classes**:

#### DataExtractor
```python
class DataExtractor:
    def __init__(self)
    def generate_sample_data(self, num_customers: int, num_products: int, num_transactions: int) -> Dict[str, pd.DataFrame]
    def load_data_to_database(self, dataframes: Dict[str, pd.DataFrame]) -> bool
    def extract_from_csv(self, file_path: str) -> pd.DataFrame
    def validate_data(self, df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, List[str]]
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame
```

**Key Features**:
- Configurable sample data generation
- Data validation and quality checks
- Automated data cleaning
- Multiple data source support

**Data Generation Parameters**:
- `num_customers`: Number of customer records to generate
- `num_products`: Number of product records to generate
- `num_transactions`: Number of transaction records to generate

**Validation Rules**:
- Required column presence
- Data type validation
- Null value detection
- Referential integrity checks

### src/data_analysis.py

**Purpose**: Core analytical functions and business intelligence

**Classes**:

#### DataAnalyzer
```python
class DataAnalyzer:
    def __init__(self)
    def get_data_from_query(self, query: str) -> pd.DataFrame
    def sales_performance_analysis(self) -> Dict[str, any]
    def customer_analysis(self) -> Dict[str, any]
    def product_analysis(self) -> Dict[str, any]
    def channel_analysis(self) -> Dict[str, any]
    def discount_analysis(self) -> Dict[str, any]
    def generate_insights(self) -> Dict[str, List[str]]
    def create_visualizations(self) -> Dict[str, any]
```

**Analysis Methods**:

**Sales Performance Analysis**:
- Total revenue and transaction metrics
- Monthly trend analysis with growth rates
- Top performing periods identification
- Seasonal pattern detection

**Customer Analysis**:
- Customer segmentation by value
- Geographic distribution analysis
- Retention and loyalty metrics
- Top customer identification

**Product Analysis**:
- Category and brand performance
- Product profitability analysis
- Price range effectiveness
- Inventory turnover metrics

**Channel Analysis**:
- Sales channel effectiveness
- Payment method preferences
- Cross-channel performance
- Operational efficiency metrics

### src/streamlit_app.py

**Purpose**: Web-based dashboard interface

**Classes**:

#### StreamlitDashboard
```python
class StreamlitDashboard:
    def __init__(self)
    def load_sample_data(self) -> None
    def render_sidebar(self) -> Tuple[str, tuple]
    def render_overview(self) -> None
    def render_sales_analysis(self) -> None
    def render_customer_analysis(self) -> None
    def render_product_analysis(self) -> None
    def render_channel_analysis(self) -> None
    def render_custom_query(self) -> None
    def run(self) -> None
```

**Dashboard Features**:
- Interactive navigation
- Real-time data filtering
- Dynamic chart generation
- Export capabilities
- Custom query interface

## API Reference

### Database Operations

#### Connection Management
```python
# Get database connection
conn = db_config.get_connection()

# Get SQLAlchemy engine
engine = db_config.get_engine()

# Execute parameterized query
results = db_config.execute_query(
    "SELECT * FROM customers WHERE state = ?", 
    ("CA",)
)
```

#### Query Execution
```python
# Simple query
df = analyzer.get_data_from_query("SELECT COUNT(*) FROM transactions")

# Complex analytical query
monthly_sales = analyzer.get_data_from_query("""
    SELECT 
        strftime('%Y-%m', transaction_date) as month,
        SUM(total_amount) as revenue
    FROM transactions
    GROUP BY strftime('%Y-%m', transaction_date)
    ORDER BY month
""")
```

### Data Analysis Functions

#### Sales Analysis
```python
# Get comprehensive sales analysis
sales_data = analyzer.sales_performance_analysis()

# Access specific metrics
total_revenue = sales_data['total_metrics']['total_revenue']
monthly_trend = sales_data['monthly_trend']
top_days = sales_data['top_performing_days']
```

#### Customer Analysis
```python
# Get customer insights
customer_data = analyzer.customer_analysis()

# Access segmentation data
segments = customer_data['segment_analysis']
top_customers = customer_data['top_customers']
geographic_dist = customer_data['geographic_distribution']
```

### Data Extraction Functions

#### Sample Data Generation
```python
# Generate sample data
extractor = DataExtractor()
sample_data = extractor.generate_sample_data(
    num_customers=100,
    num_products=50,
    num_transactions=1000
)

# Load to database
success = extractor.load_data_to_database(sample_data)
```

#### Data Validation
```python
# Validate dataframe
required_cols = ['customer_id', 'first_name', 'email']
is_valid, issues = extractor.validate_data(df, required_cols)

if not is_valid:
    print("Validation issues:", issues)
```

## Performance Optimization

### Database Optimization

**Indexing Strategy**:
```sql
-- Primary indexes for frequent queries
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_customers_segment ON customers(customer_segment);

-- Composite indexes for complex queries
CREATE INDEX idx_transactions_date_customer ON transactions(transaction_date, customer_id);
```

**Query Optimization**:
- Use appropriate WHERE clauses
- Limit result sets with LIMIT
- Use EXISTS instead of IN for subqueries
- Avoid SELECT * in production queries

**Connection Management**:
```python
# Use context managers for connections
with db_config.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
# Connection automatically closed
```

### Application Performance

**Caching Strategy**:
```python
# Cache analysis results in session state
if 'sales_analysis' not in st.session_state:
    st.session_state.sales_analysis = analyzer.sales_performance_analysis()

# Use cached results
sales_data = st.session_state.sales_analysis
```

**Memory Management**:
- Use generators for large datasets
- Implement pagination for large result sets
- Clear unused variables and dataframes
- Monitor memory usage in production

**Visualization Optimization**:
```python
# Limit data points for charts
if len(data) > 1000:
    data = data.sample(n=1000)

# Use appropriate chart types
# Line charts for time series
# Bar charts for categories
# Pie charts for proportions
```

## Security Considerations

### SQL Injection Prevention

**Parameterized Queries**:
```python
# GOOD: Parameterized query
query = "SELECT * FROM customers WHERE state = ?"
results = db_config.execute_query(query, (state_value,))

# BAD: String concatenation
query = f"SELECT * FROM customers WHERE state = '{state_value}'"
```

**Query Validation**:
```python
# Block dangerous operations
dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'ALTER', 'CREATE']
if any(keyword in query.upper() for keyword in dangerous_keywords):
    raise ValueError("Modification queries not allowed")
```

### Data Protection

**Sensitive Data Handling**:
- Mask personal information in displays
- Implement data anonymization for demos
- Use environment variables for configuration
- Secure database file permissions

**Access Control**:
```python
# Future enhancement: Role-based access
def check_user_permission(user_role, operation):
    permissions = {
        'viewer': ['read'],
        'analyst': ['read', 'query'],
        'admin': ['read', 'query', 'modify']
    }
    return operation in permissions.get(user_role, [])
```

## Deployment Guide

### Local Development Setup

1. **Environment Setup**:
   ```bash
   python -m venv analytics_env
   source analytics_env/bin/activate  # Linux/Mac
   # or
   analytics_env\Scripts\activate     # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**:
   ```bash
   python src/data_extraction.py
   ```

4. **Run Application**:
   ```bash
   streamlit run src/streamlit_app.py
   ```

### Production Deployment

**Docker Deployment**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Environment Configuration**:
```bash
# Production environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export DATABASE_PATH=/data/analytics.db
```

### Cloud Deployment Options

**Streamlit Cloud**:
- Direct GitHub integration
- Automatic deployments
- Built-in authentication
- Free tier available

**AWS Deployment**:
- EC2 instance with Docker
- RDS for database (PostgreSQL)
- Application Load Balancer
- CloudWatch monitoring

**Azure Deployment**:
- Azure Container Instances
- Azure Database for PostgreSQL
- Application Gateway
- Azure Monitor

## Extension Guidelines

### Adding New Analysis Types

1. **Create Analysis Method**:
   ```python
   def new_analysis_type(self) -> Dict[str, any]:
       """New analysis implementation."""
       query = """
       SELECT ... FROM ... WHERE ...
       """
       data = self.get_data_from_query(query)
       
       # Process data
       results = process_analysis_data(data)
       
       return {
           'analysis_results': results,
           'metadata': {...}
       }
   ```

2. **Add Dashboard Page**:
   ```python
   def render_new_analysis(self):
       """Render new analysis dashboard."""
       st.header("New Analysis Type")
       
       # Get analysis data
       analysis_data = self.analyzer.new_analysis_type()
       
       # Create visualizations
       fig = create_visualization(analysis_data)
       st.plotly_chart(fig)
   ```

3. **Update Navigation**:
   ```python
   page = st.sidebar.selectbox(
       "Select Analysis",
       ["Overview", "Sales Analysis", ..., "New Analysis"]
   )
   ```

### Database Schema Extensions

**Adding New Tables**:
```sql
-- Add to schema.sql
CREATE TABLE new_table (
    id INTEGER PRIMARY KEY,
    -- other columns
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add appropriate indexes
CREATE INDEX idx_new_table_column ON new_table(column_name);
```

**Modifying Existing Tables**:
```sql
-- Create migration script
ALTER TABLE existing_table ADD COLUMN new_column TEXT;
UPDATE existing_table SET new_column = 'default_value';
```

### Custom Data Sources

1. **Extend DataExtractor**:
   ```python
   def extract_from_api(self, api_url: str, headers: dict) -> pd.DataFrame:
       """Extract data from API endpoint."""
       response = requests.get(api_url, headers=headers)
       data = response.json()
       return pd.DataFrame(data)
   ```

2. **Add Validation Rules**:
   ```python
   def validate_api_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
       """Validate API-specific data format."""
       # Custom validation logic
       pass
   ```

### Testing Extensions

**Unit Tests for New Features**:
```python
def test_new_analysis_type(self, analyzer_with_data):
    """Test new analysis functionality."""
    analyzer, _ = analyzer_with_data
    
    results = analyzer.new_analysis_type()
    
    assert 'analysis_results' in results
    assert isinstance(results['analysis_results'], pd.DataFrame)
    assert len(results['analysis_results']) > 0
```

**Integration Tests**:
```python
def test_new_dashboard_page(self):
    """Test new dashboard page rendering."""
    # Test dashboard functionality
    pass
```

### Performance Considerations for Extensions

**Query Optimization**:
- Add appropriate indexes for new queries
- Use EXPLAIN QUERY PLAN to analyze performance
- Implement query result caching
- Consider data partitioning for large datasets

**Memory Management**:
- Stream large datasets instead of loading entirely
- Implement pagination for UI components
- Use efficient data structures
- Monitor memory usage

**Scalability Planning**:
- Design for horizontal scaling
- Consider database sharding strategies
- Implement connection pooling
- Plan for concurrent user access

---

This technical documentation provides comprehensive information for developers working with or extending the Business Analytics project. For user-focused information, refer to the User Guide. For project overview and setup instructions, see the main README.