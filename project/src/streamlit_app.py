"""
Streamlit web application for interactive data analysis dashboard.
This application provides a comprehensive interface for exploring business analytics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List

# Import custom modules
from data_analysis import DataAnalyzer
from data_extraction import DataExtractor
from config.database_config import db_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitDashboard:
    """Main dashboard class for Streamlit application."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.analyzer = DataAnalyzer()
        self.extractor = DataExtractor()
        
        # Initialize session state
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
        if 'analysis_cache' not in st.session_state:
            st.session_state.analysis_cache = {}
    
    def load_sample_data(self):
        """Load sample data into the database."""
        try:
            with st.spinner("Loading sample data..."):
                # Initialize database schema
                db_config.execute_script('sql/schema.sql')
                
                # Generate sample data
                sample_data = self.extractor.generate_sample_data(
                    num_customers=200,
                    num_products=100,
                    num_transactions=2000
                )
                
                # Load to database
                success = self.extractor.load_data_to_database(sample_data)
                
                if success:
                    st.session_state.data_loaded = True
                    st.success("Sample data loaded successfully!")
                else:
                    st.error("Failed to load sample data")
                    
        except Exception as e:
            st.error(f"Error loading data: {e}")
            logger.error(f"Error loading sample data: {e}")
    
    def render_sidebar(self):
        """Render the sidebar with navigation and controls."""
        st.sidebar.title("📊 Analytics Dashboard")
        
        # Data loading section
        st.sidebar.header("Data Management")
        if not st.session_state.data_loaded:
            if st.sidebar.button("Load Sample Data", type="primary"):
                self.load_sample_data()
        else:
            st.sidebar.success("✅ Data loaded")
            if st.sidebar.button("Reload Data"):
                self.load_sample_data()
        
        # Navigation
        st.sidebar.header("Navigation")
        page = st.sidebar.selectbox(
            "Select Analysis",
            ["Overview", "Sales Analysis", "Customer Analysis", 
             "Product Analysis", "Channel Analysis", "Custom Query"]
        )
        
        # Filters
        st.sidebar.header("Filters")
        
        # Date range filter
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=90), datetime.now()),
            max_value=datetime.now()
        )
        
        return page, date_range
    
    def render_overview(self):
        """Render the overview dashboard."""
        st.markdown('<h1 class="main-header">Business Analytics Overview</h1>', unsafe_allow_html=True)
        
        if not st.session_state.data_loaded:
            st.warning("Please load sample data from the sidebar to begin analysis.")
            return
        
        try:
            # Get key metrics
            sales_data = self.analyzer.sales_performance_analysis()
            customer_data = self.analyzer.customer_analysis()
            product_data = self.analyzer.product_analysis()
            
            # Key metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Revenue",
                    f"${sales_data['total_metrics']['total_revenue']:,.2f}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Total Transactions",
                    f"{sales_data['total_metrics']['total_transactions']:,}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "Average Order Value",
                    f"${sales_data['total_metrics']['avg_order_value']:.2f}",
                    delta=None
                )
            
            with col4:
                st.metric(
                    "Unique Customers",
                    f"{sales_data['total_metrics']['unique_customers']:,}",
                    delta=None
                )
            
            # Charts row
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly sales trend
                monthly_data = sales_data['monthly_trend']
                if not monthly_data.empty:
                    fig_trend = px.line(
                        monthly_data, x='month', y='revenue',
                        title='Monthly Revenue Trend',
                        labels={'revenue': 'Revenue ($)', 'month': 'Month'}
                    )
                    fig_trend.update_layout(height=400)
                    st.plotly_chart(fig_trend, use_container_width=True)
            
            with col2:
                # Customer segments
                segment_data = customer_data['segment_analysis']
                if not segment_data.empty:
                    fig_segments = px.pie(
                        segment_data, values='customer_count', names='customer_segment',
                        title='Customer Distribution by Segment'
                    )
                    fig_segments.update_layout(height=400)
                    st.plotly_chart(fig_segments, use_container_width=True)
            
            # Product category performance
            category_data = product_data['category_performance']
            if not category_data.empty:
                fig_categories = px.bar(
                    category_data, x='category', y='total_revenue',
                    title='Revenue by Product Category',
                    labels={'total_revenue': 'Revenue ($)', 'category': 'Category'}
                )
                fig_categories.update_layout(height=400)
                st.plotly_chart(fig_categories, use_container_width=True)
            
            # Business insights
            st.subheader("🔍 Key Insights")
            insights = self.analyzer.generate_insights()
            
            for category, insight_list in insights.items():
                if insight_list:
                    st.markdown(f"**{category.replace('_', ' ').title()}:**")
                    for insight in insight_list:
                        st.markdown(f"• {insight}")
                    st.markdown("---")
            
        except Exception as e:
            st.error(f"Error rendering overview: {e}")
            logger.error(f"Error in overview: {e}")
    
    def render_sales_analysis(self):
        """Render detailed sales analysis."""
        st.header("📈 Sales Performance Analysis")
        
        if not st.session_state.data_loaded:
            st.warning("Please load sample data from the sidebar.")
            return
        
        try:
            sales_data = self.analyzer.sales_performance_analysis()
            
            # Detailed metrics
            st.subheader("Sales Metrics")
            metrics = sales_data['total_metrics']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Revenue", f"${metrics['total_revenue']:,.2f}")
                st.metric("Total Transactions", f"{metrics['total_transactions']:,}")
            
            with col2:
                st.metric("Average Order Value", f"${metrics['avg_order_value']:.2f}")
                st.metric("Total Items Sold", f"{metrics['total_items_sold']:,}")
            
            with col3:
                st.metric("Unique Customers", f"{metrics['unique_customers']:,}")
                date_range = (pd.to_datetime(metrics['last_sale_date']) - pd.to_datetime(metrics['first_sale_date'])).days
                st.metric("Analysis Period (Days)", f"{date_range}")
            
            # Monthly trend with growth rates
            st.subheader("Monthly Sales Trend")
            monthly_data = sales_data['monthly_trend']
            
            if not monthly_data.empty and len(monthly_data) > 1:
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Revenue Trend', 'Growth Rate'),
                    vertical_spacing=0.1
                )
                
                # Revenue trend
                fig.add_trace(
                    go.Scatter(x=monthly_data['month'], y=monthly_data['revenue'],
                             mode='lines+markers', name='Revenue'),
                    row=1, col=1
                )
                
                # Growth rate
                if 'revenue_growth' in monthly_data.columns:
                    fig.add_trace(
                        go.Bar(x=monthly_data['month'], y=monthly_data['revenue_growth'],
                             name='Growth Rate (%)'),
                        row=2, col=1
                    )
                
                fig.update_layout(height=600, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
            
            # Top performing days
            st.subheader("Top Performing Days")
            top_days = sales_data['top_performing_days']
            if not top_days.empty:
                st.dataframe(top_days, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error in sales analysis: {e}")
    
    def render_customer_analysis(self):
        """Render customer analysis dashboard."""
        st.header("👥 Customer Analysis")
        
        if not st.session_state.data_loaded:
            st.warning("Please load sample data from the sidebar.")
            return
        
        try:
            customer_data = self.analyzer.customer_analysis()
            
            # Customer segments
            st.subheader("Customer Segmentation")
            segment_data = customer_data['segment_analysis']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if not segment_data.empty:
                    fig_segments = px.bar(
                        segment_data, x='customer_segment', y='avg_customer_value',
                        title='Average Customer Value by Segment',
                        color='customer_segment'
                    )
                    st.plotly_chart(fig_segments, use_container_width=True)
            
            with col2:
                if not segment_data.empty:
                    fig_count = px.pie(
                        segment_data, values='customer_count', names='customer_segment',
                        title='Customer Count by Segment'
                    )
                    st.plotly_chart(fig_count, use_container_width=True)
            
            # Top customers
            st.subheader("Top Customers")
            top_customers = customer_data['top_customers']
            if not top_customers.empty:
                st.dataframe(
                    top_customers.head(10),
                    column_config={
                        "total_spent": st.column_config.NumberColumn(
                            "Total Spent",
                            format="$%.2f"
                        ),
                        "avg_order_value": st.column_config.NumberColumn(
                            "Avg Order Value",
                            format="$%.2f"
                        )
                    },
                    use_container_width=True
                )
            
            # Geographic distribution
            st.subheader("Geographic Distribution")
            geo_data = customer_data['geographic_distribution']
            if not geo_data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_geo = px.bar(
                        geo_data.head(10), x='state', y='total_revenue',
                        title='Revenue by State',
                        labels={'total_revenue': 'Revenue ($)', 'state': 'State'}
                    )
                    st.plotly_chart(fig_geo, use_container_width=True)
                
                with col2:
                    fig_customers = px.bar(
                        geo_data.head(10), x='state', y='customer_count',
                        title='Customer Count by State',
                        labels={'customer_count': 'Customers', 'state': 'State'}
                    )
                    st.plotly_chart(fig_customers, use_container_width=True)
            
            # Customer retention
            st.subheader("Customer Retention Analysis")
            retention_data = customer_data['retention_analysis']
            if not retention_data.empty:
                fig_retention = px.bar(
                    retention_data, x='active_months', y='customer_count',
                    title='Customer Activity Distribution',
                    labels={'active_months': 'Active Months', 'customer_count': 'Customer Count'}
                )
                st.plotly_chart(fig_retention, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error in customer analysis: {e}")
    
    def render_product_analysis(self):
        """Render product analysis dashboard."""
        st.header("🛍️ Product Analysis")
        
        if not st.session_state.data_loaded:
            st.warning("Please load sample data from the sidebar.")
            return
        
        try:
            product_data = self.analyzer.product_analysis()
            
            # Category performance
            st.subheader("Category Performance")
            category_data = product_data['category_performance']
            
            if not category_data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_revenue = px.pie(
                        category_data, values='total_revenue', names='category',
                        title='Revenue Distribution by Category'
                    )
                    st.plotly_chart(fig_revenue, use_container_width=True)
                
                with col2:
                    fig_sales = px.bar(
                        category_data, x='category', y='total_sales',
                        title='Sales Count by Category',
                        labels={'total_sales': 'Sales Count', 'category': 'Category'}
                    )
                    st.plotly_chart(fig_sales, use_container_width=True)
            
            # Top products
            st.subheader("Top Performing Products")
            top_products = product_data['top_products']
            if not top_products.empty:
                st.dataframe(
                    top_products.head(15),
                    column_config={
                        "price": st.column_config.NumberColumn("Price", format="$%.2f"),
                        "total_revenue": st.column_config.NumberColumn("Revenue", format="$%.2f"),
                        "total_profit": st.column_config.NumberColumn("Profit", format="$%.2f")
                    },
                    use_container_width=True
                )
            
            # Brand analysis
            st.subheader("Brand Performance")
            brand_data = product_data['brand_analysis']
            if not brand_data.empty:
                fig_brands = px.bar(
                    brand_data, x='brand', y='total_revenue',
                    title='Revenue by Brand',
                    labels={'total_revenue': 'Revenue ($)', 'brand': 'Brand'}
                )
                st.plotly_chart(fig_brands, use_container_width=True)
            
            # Price analysis
            st.subheader("Price Range Analysis")
            price_data = product_data['price_analysis']
            if not price_data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_price_revenue = px.bar(
                        price_data, x='price_range', y='total_revenue',
                        title='Revenue by Price Range'
                    )
                    st.plotly_chart(fig_price_revenue, use_container_width=True)
                
                with col2:
                    fig_price_avg = px.bar(
                        price_data, x='price_range', y='avg_order_value',
                        title='Average Order Value by Price Range'
                    )
                    st.plotly_chart(fig_price_avg, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error in product analysis: {e}")
    
    def render_channel_analysis(self):
        """Render channel and payment analysis."""
        st.header("🚀 Channel & Payment Analysis")
        
        if not st.session_state.data_loaded:
            st.warning("Please load sample data from the sidebar.")
            return
        
        try:
            channel_data = self.analyzer.channel_analysis()
            
            # Sales channel performance
            st.subheader("Sales Channel Performance")
            channel_perf = channel_data['channel_performance']
            
            if not channel_perf.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_channel_revenue = px.pie(
                        channel_perf, values='total_revenue', names='sales_channel',
                        title='Revenue Distribution by Channel'
                    )
                    st.plotly_chart(fig_channel_revenue, use_container_width=True)
                
                with col2:
                    fig_channel_transactions = px.bar(
                        channel_perf, x='sales_channel', y='transaction_count',
                        title='Transaction Count by Channel'
                    )
                    st.plotly_chart(fig_channel_transactions, use_container_width=True)
            
            # Payment method analysis
            st.subheader("Payment Method Analysis")
            payment_data = channel_data['payment_analysis']
            
            if not payment_data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_payment = px.pie(
                        payment_data, values='transaction_count', names='payment_method',
                        title='Transaction Distribution by Payment Method'
                    )
                    st.plotly_chart(fig_payment, use_container_width=True)
                
                with col2:
                    fig_payment_value = px.bar(
                        payment_data, x='payment_method', y='avg_transaction_value',
                        title='Average Transaction Value by Payment Method'
                    )
                    st.plotly_chart(fig_payment_value, use_container_width=True)
            
            # Cross analysis
            st.subheader("Channel-Payment Cross Analysis")
            cross_data = channel_data['cross_analysis']
            if not cross_data.empty:
                # Create pivot table for heatmap
                pivot_data = cross_data.pivot(
                    index='sales_channel', 
                    columns='payment_method', 
                    values='total_revenue'
                ).fillna(0)
                
                fig_heatmap = px.imshow(
                    pivot_data,
                    title='Revenue Heatmap: Channel vs Payment Method',
                    labels=dict(x="Payment Method", y="Sales Channel", color="Revenue")
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error in channel analysis: {e}")
    
    def render_custom_query(self):
        """Render custom SQL query interface."""
        st.header("🔍 Custom Query Interface")
        
        if not st.session_state.data_loaded:
            st.warning("Please load sample data from the sidebar.")
            return
        
        st.subheader("Execute Custom SQL Query")
        
        # Sample queries
        sample_queries = {
            "Top 10 Customers by Revenue": """
                SELECT 
                    c.first_name || ' ' || c.last_name as customer_name,
                    SUM(t.total_amount) as total_spent,
                    COUNT(t.transaction_id) as total_orders
                FROM customers c
                JOIN transactions t ON c.customer_id = t.customer_id
                GROUP BY c.customer_id
                ORDER BY total_spent DESC
                LIMIT 10;
            """,
            "Monthly Sales Summary": """
                SELECT 
                    strftime('%Y-%m', transaction_date) as month,
                    COUNT(transaction_id) as transactions,
                    SUM(total_amount) as revenue,
                    AVG(total_amount) as avg_order_value
                FROM transactions
                GROUP BY strftime('%Y-%m', transaction_date)
                ORDER BY month;
            """,
            "Product Performance": """
                SELECT 
                    p.product_name,
                    p.category,
                    COUNT(t.transaction_id) as sales_count,
                    SUM(t.total_amount) as total_revenue
                FROM products p
                JOIN transactions t ON p.product_id = t.product_id
                GROUP BY p.product_id
                ORDER BY total_revenue DESC
                LIMIT 15;
            """
        }
        
        # Query selector
        selected_query = st.selectbox("Select a sample query:", list(sample_queries.keys()))
        
        # Query input
        query = st.text_area(
            "SQL Query:",
            value=sample_queries[selected_query],
            height=200,
            help="Enter your SQL query here. Be careful with UPDATE/DELETE operations."
        )
        
        if st.button("Execute Query", type="primary"):
            try:
                # Basic validation
                if query.strip().upper().startswith(('UPDATE', 'DELETE', 'DROP', 'ALTER')):
                    st.error("Modification queries are not allowed for safety reasons.")
                    return
                
                # Execute query
                result_df = self.analyzer.get_data_from_query(query)
                
                if not result_df.empty:
                    st.success(f"Query executed successfully! Retrieved {len(result_df)} rows.")
                    
                    # Display results
                    st.subheader("Query Results")
                    st.dataframe(result_df, use_container_width=True)
                    
                    # Download option
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("Query executed successfully but returned no results.")
                    
            except Exception as e:
                st.error(f"Error executing query: {e}")
    
    def run(self):
        """Run the Streamlit dashboard."""
        # Render sidebar and get selections
        page, date_range = self.render_sidebar()
        
        # Render selected page
        if page == "Overview":
            self.render_overview()
        elif page == "Sales Analysis":
            self.render_sales_analysis()
        elif page == "Customer Analysis":
            self.render_customer_analysis()
        elif page == "Product Analysis":
            self.render_product_analysis()
        elif page == "Channel Analysis":
            self.render_channel_analysis()
        elif page == "Custom Query":
            self.render_custom_query()

def main():
    """Main function to run the Streamlit app."""
    dashboard = StreamlitDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()