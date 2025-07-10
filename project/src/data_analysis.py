"""
Data analysis module containing core analytical functions and statistical computations.
This module provides comprehensive analysis capabilities for business intelligence.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple, Optional
from config.database_config import db_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DataAnalyzer:
    """Comprehensive data analysis class for business intelligence."""
    
    def __init__(self):
        """Initialize the data analyzer."""
        self.db_config = db_config
        
    def get_data_from_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame.
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            pd.DataFrame: Query results
        """
        try:
            engine = self.db_config.get_engine()
            df = pd.read_sql_query(query, engine)
            return df
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
    
    def sales_performance_analysis(self) -> Dict[str, any]:
        """
        Analyze overall sales performance metrics.
        
        Returns:
            Dict[str, any]: Sales performance insights
        """
        logger.info("Performing sales performance analysis")
        
        # Total sales metrics
        total_sales_query = """
        SELECT 
            COUNT(transaction_id) as total_transactions,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers,
            SUM(quantity) as total_items_sold,
            MIN(transaction_date) as first_sale_date,
            MAX(transaction_date) as last_sale_date
        FROM transactions;
        """
        
        total_metrics = self.get_data_from_query(total_sales_query).iloc[0]
        
        # Monthly trend analysis
        monthly_trend_query = """
        SELECT 
            strftime('%Y-%m', transaction_date) as month,
            COUNT(transaction_id) as transactions,
            SUM(total_amount) as revenue,
            AVG(total_amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM transactions
        GROUP BY strftime('%Y-%m', transaction_date)
        ORDER BY month;
        """
        
        monthly_trend = self.get_data_from_query(monthly_trend_query)
        
        # Calculate growth rates
        if len(monthly_trend) > 1:
            monthly_trend['revenue_growth'] = monthly_trend['revenue'].pct_change() * 100
            monthly_trend['transaction_growth'] = monthly_trend['transactions'].pct_change() * 100
        
        # Top performing days
        daily_performance_query = """
        SELECT 
            DATE(transaction_date) as date,
            COUNT(transaction_id) as transactions,
            SUM(total_amount) as revenue
        FROM transactions
        GROUP BY DATE(transaction_date)
        ORDER BY revenue DESC
        LIMIT 10;
        """
        
        top_days = self.get_data_from_query(daily_performance_query)
        
        return {
            'total_metrics': total_metrics.to_dict(),
            'monthly_trend': monthly_trend,
            'top_performing_days': top_days,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def customer_analysis(self) -> Dict[str, any]:
        """
        Analyze customer behavior and segmentation.
        
        Returns:
            Dict[str, any]: Customer analysis insights
        """
        logger.info("Performing customer analysis")
        
        # Customer segmentation analysis
        segment_query = """
        SELECT 
            customer_segment,
            COUNT(*) as customer_count,
            AVG(total_spent) as avg_customer_value,
            AVG(total_transactions) as avg_transactions,
            AVG(avg_order_value) as avg_order_value
        FROM customer_metrics
        GROUP BY customer_segment
        ORDER BY avg_customer_value DESC;
        """
        
        segment_analysis = self.get_data_from_query(segment_query)
        
        # Top customers
        top_customers_query = """
        SELECT 
            customer_name,
            customer_segment,
            total_spent,
            total_transactions,
            avg_order_value,
            last_purchase_date
        FROM customer_metrics
        ORDER BY total_spent DESC
        LIMIT 20;
        """
        
        top_customers = self.get_data_from_query(top_customers_query)
        
        # Customer retention analysis
        retention_query = """
        WITH customer_months AS (
            SELECT 
                customer_id,
                COUNT(DISTINCT strftime('%Y-%m', transaction_date)) as active_months
            FROM transactions
            GROUP BY customer_id
        )
        SELECT 
            active_months,
            COUNT(*) as customer_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT customer_id) FROM transactions), 2) as percentage
        FROM customer_months
        GROUP BY active_months
        ORDER BY active_months;
        """
        
        retention_analysis = self.get_data_from_query(retention_query)
        
        # Geographic distribution
        geographic_query = """
        SELECT 
            c.state,
            COUNT(DISTINCT c.customer_id) as customer_count,
            SUM(t.total_amount) as total_revenue,
            AVG(t.total_amount) as avg_order_value
        FROM customers c
        JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY c.state
        ORDER BY total_revenue DESC;
        """
        
        geographic_analysis = self.get_data_from_query(geographic_query)
        
        return {
            'segment_analysis': segment_analysis,
            'top_customers': top_customers,
            'retention_analysis': retention_analysis,
            'geographic_distribution': geographic_analysis
        }
    
    def product_analysis(self) -> Dict[str, any]:
        """
        Analyze product performance and trends.
        
        Returns:
            Dict[str, any]: Product analysis insights
        """
        logger.info("Performing product analysis")
        
        # Category performance
        category_query = """
        SELECT 
            p.category,
            COUNT(t.transaction_id) as total_sales,
            SUM(t.total_amount) as total_revenue,
            AVG(t.total_amount) as avg_sale_amount,
            SUM(t.quantity) as total_quantity,
            COUNT(DISTINCT t.customer_id) as unique_customers
        FROM products p
        JOIN transactions t ON p.product_id = t.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
        """
        
        category_performance = self.get_data_from_query(category_query)
        
        # Top products
        top_products_query = """
        SELECT 
            p.product_name,
            p.category,
            p.brand,
            p.price,
            COUNT(t.transaction_id) as times_sold,
            SUM(t.quantity) as total_quantity,
            SUM(t.total_amount) as total_revenue,
            ROUND((p.price - p.cost) * SUM(t.quantity), 2) as total_profit
        FROM products p
        JOIN transactions t ON p.product_id = t.product_id
        GROUP BY p.product_id
        ORDER BY total_revenue DESC
        LIMIT 20;
        """
        
        top_products = self.get_data_from_query(top_products_query)
        
        # Brand analysis
        brand_query = """
        SELECT 
            p.brand,
            COUNT(DISTINCT p.product_id) as product_count,
            COUNT(t.transaction_id) as total_sales,
            SUM(t.total_amount) as total_revenue,
            AVG(t.total_amount) as avg_sale_amount
        FROM products p
        JOIN transactions t ON p.product_id = t.product_id
        GROUP BY p.brand
        ORDER BY total_revenue DESC;
        """
        
        brand_analysis = self.get_data_from_query(brand_query)
        
        # Price analysis
        price_analysis_query = """
        SELECT 
            CASE 
                WHEN p.price < 50 THEN 'Low (< $50)'
                WHEN p.price < 100 THEN 'Medium ($50-$100)'
                WHEN p.price < 200 THEN 'High ($100-$200)'
                ELSE 'Premium (> $200)'
            END as price_range,
            COUNT(t.transaction_id) as sales_count,
            SUM(t.total_amount) as total_revenue,
            AVG(t.total_amount) as avg_order_value
        FROM products p
        JOIN transactions t ON p.product_id = t.product_id
        GROUP BY price_range
        ORDER BY avg_order_value DESC;
        """
        
        price_analysis = self.get_data_from_query(price_analysis_query)
        
        return {
            'category_performance': category_performance,
            'top_products': top_products,
            'brand_analysis': brand_analysis,
            'price_analysis': price_analysis
        }
    
    def channel_analysis(self) -> Dict[str, any]:
        """
        Analyze sales channels and payment methods.
        
        Returns:
            Dict[str, any]: Channel analysis insights
        """
        logger.info("Performing channel analysis")
        
        # Sales channel performance
        channel_query = """
        SELECT 
            sales_channel,
            COUNT(transaction_id) as transaction_count,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value,
            COUNT(DISTINCT customer_id) as unique_customers,
            ROUND(COUNT(transaction_id) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as percentage
        FROM transactions
        GROUP BY sales_channel
        ORDER BY total_revenue DESC;
        """
        
        channel_performance = self.get_data_from_query(channel_query)
        
        # Payment method analysis
        payment_query = """
        SELECT 
            payment_method,
            COUNT(transaction_id) as transaction_count,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_transaction_value,
            ROUND(COUNT(transaction_id) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as usage_percentage
        FROM transactions
        GROUP BY payment_method
        ORDER BY transaction_count DESC;
        """
        
        payment_analysis = self.get_data_from_query(payment_query)
        
        # Channel-Payment cross analysis
        cross_analysis_query = """
        SELECT 
            sales_channel,
            payment_method,
            COUNT(transaction_id) as transaction_count,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order_value
        FROM transactions
        GROUP BY sales_channel, payment_method
        ORDER BY total_revenue DESC;
        """
        
        cross_analysis = self.get_data_from_query(cross_analysis_query)
        
        return {
            'channel_performance': channel_performance,
            'payment_analysis': payment_analysis,
            'cross_analysis': cross_analysis
        }
    
    def discount_analysis(self) -> Dict[str, any]:
        """
        Analyze discount impact on sales.
        
        Returns:
            Dict[str, any]: Discount analysis insights
        """
        logger.info("Performing discount analysis")
        
        discount_query = """
        SELECT 
            CASE 
                WHEN discount_amount = 0 THEN 'No Discount'
                WHEN discount_amount <= 10 THEN 'Low (≤$10)'
                WHEN discount_amount <= 25 THEN 'Medium ($11-$25)'
                ELSE 'High (>$25)'
            END as discount_category,
            COUNT(transaction_id) as transaction_count,
            AVG(total_amount) as avg_order_value,
            AVG(quantity) as avg_items_per_order,
            SUM(total_amount) as total_revenue,
            AVG(discount_amount) as avg_discount
        FROM transactions
        GROUP BY discount_category
        ORDER BY avg_order_value DESC;
        """
        
        discount_impact = self.get_data_from_query(discount_query)
        
        return {'discount_impact': discount_impact}
    
    def generate_insights(self) -> Dict[str, List[str]]:
        """
        Generate business insights based on analysis results.
        
        Returns:
            Dict[str, List[str]]: Categorized business insights
        """
        logger.info("Generating business insights")
        
        insights = {
            'sales_insights': [],
            'customer_insights': [],
            'product_insights': [],
            'operational_insights': []
        }
        
        try:
            # Sales insights
            sales_data = self.sales_performance_analysis()
            total_revenue = sales_data['total_metrics']['total_revenue']
            avg_order_value = sales_data['total_metrics']['avg_order_value']
            
            insights['sales_insights'].append(f"Total revenue generated: ${total_revenue:,.2f}")
            insights['sales_insights'].append(f"Average order value: ${avg_order_value:.2f}")
            
            if len(sales_data['monthly_trend']) > 1:
                latest_growth = sales_data['monthly_trend']['revenue_growth'].iloc[-1]
                if not pd.isna(latest_growth):
                    if latest_growth > 0:
                        insights['sales_insights'].append(f"Revenue growth in latest month: +{latest_growth:.1f}%")
                    else:
                        insights['sales_insights'].append(f"Revenue decline in latest month: {latest_growth:.1f}%")
            
            # Customer insights
            customer_data = self.customer_analysis()
            top_segment = customer_data['segment_analysis'].iloc[0]
            insights['customer_insights'].append(f"Highest value segment: {top_segment['customer_segment']} (${top_segment['avg_customer_value']:.2f} avg)")
            
            # Product insights
            product_data = self.product_analysis()
            top_category = product_data['category_performance'].iloc[0]
            insights['product_insights'].append(f"Top performing category: {top_category['category']} (${top_category['total_revenue']:,.2f} revenue)")
            
            # Channel insights
            channel_data = self.channel_analysis()
            top_channel = channel_data['channel_performance'].iloc[0]
            insights['operational_insights'].append(f"Most effective sales channel: {top_channel['sales_channel']} ({top_channel['percentage']:.1f}% of transactions)")
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            insights['operational_insights'].append("Unable to generate some insights due to data limitations")
        
        return insights
    
    def create_visualizations(self) -> Dict[str, any]:
        """
        Create comprehensive visualizations for the analysis.
        
        Returns:
            Dict[str, any]: Dictionary containing visualization objects
        """
        logger.info("Creating visualizations")
        
        visualizations = {}
        
        try:
            # Sales trend visualization
            sales_data = self.sales_performance_analysis()
            monthly_trend = sales_data['monthly_trend']
            
            if not monthly_trend.empty:
                fig_sales = px.line(monthly_trend, x='month', y='revenue', 
                                  title='Monthly Sales Revenue Trend',
                                  labels={'revenue': 'Revenue ($)', 'month': 'Month'})
                fig_sales.update_layout(xaxis_tickangle=-45)
                visualizations['sales_trend'] = fig_sales
            
            # Customer segment analysis
            customer_data = self.customer_analysis()
            segment_data = customer_data['segment_analysis']
            
            if not segment_data.empty:
                fig_segments = px.bar(segment_data, x='customer_segment', y='avg_customer_value',
                                    title='Average Customer Value by Segment',
                                    labels={'avg_customer_value': 'Average Customer Value ($)', 
                                           'customer_segment': 'Customer Segment'})
                visualizations['customer_segments'] = fig_segments
            
            # Product category performance
            product_data = self.product_analysis()
            category_data = product_data['category_performance']
            
            if not category_data.empty:
                fig_categories = px.pie(category_data, values='total_revenue', names='category',
                                      title='Revenue Distribution by Product Category')
                visualizations['category_distribution'] = fig_categories
            
            # Channel performance
            channel_data = self.channel_analysis()
            channel_performance = channel_data['channel_performance']
            
            if not channel_performance.empty:
                fig_channels = px.bar(channel_performance, x='sales_channel', y='total_revenue',
                                    title='Revenue by Sales Channel',
                                    labels={'total_revenue': 'Total Revenue ($)', 
                                           'sales_channel': 'Sales Channel'})
                visualizations['channel_performance'] = fig_channels
            
        except Exception as e:
            logger.error(f"Error creating visualizations: {e}")
        
        return visualizations

def main():
    """Main function to demonstrate data analysis."""
    analyzer = DataAnalyzer()
    
    # Perform comprehensive analysis
    print("=== SALES PERFORMANCE ANALYSIS ===")
    sales_results = analyzer.sales_performance_analysis()
    print(f"Total Revenue: ${sales_results['total_metrics']['total_revenue']:,.2f}")
    print(f"Total Transactions: {sales_results['total_metrics']['total_transactions']:,}")
    print(f"Average Order Value: ${sales_results['total_metrics']['avg_order_value']:.2f}")
    
    print("\n=== CUSTOMER ANALYSIS ===")
    customer_results = analyzer.customer_analysis()
    print("Top Customer Segments:")
    print(customer_results['segment_analysis'].to_string(index=False))
    
    print("\n=== PRODUCT ANALYSIS ===")
    product_results = analyzer.product_analysis()
    print("Top Product Categories:")
    print(product_results['category_performance'].to_string(index=False))
    
    print("\n=== BUSINESS INSIGHTS ===")
    insights = analyzer.generate_insights()
    for category, insight_list in insights.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for insight in insight_list:
            print(f"  • {insight}")

if __name__ == "__main__":
    main()