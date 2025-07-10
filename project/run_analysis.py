#!/usr/bin/env python3
"""
Main script to run the complete data analysis pipeline.
This script demonstrates the full workflow from data extraction to analysis.
"""

import sys
import os
import logging
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_extraction import DataExtractor
from data_analysis import DataAnalyzer
from config.database_config import db_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the complete analysis pipeline."""
    logger.info("Starting Business Analytics Pipeline")
    
    try:
        # Step 1: Initialize Database
        logger.info("Step 1: Initializing database schema")
        db_config.execute_script('sql/schema.sql')
        logger.info("Database schema initialized successfully")
        
        # Step 2: Extract and Load Data
        logger.info("Step 2: Extracting and loading sample data")
        extractor = DataExtractor()
        
        # Generate sample data
        sample_data = extractor.generate_sample_data(
            num_customers=200,
            num_products=100,
            num_transactions=2000
        )
        
        # Load data to database
        success = extractor.load_data_to_database(sample_data)
        if not success:
            raise Exception("Failed to load data to database")
        
        logger.info("Sample data loaded successfully")
        
        # Step 3: Perform Analysis
        logger.info("Step 3: Performing comprehensive data analysis")
        analyzer = DataAnalyzer()
        
        # Sales Performance Analysis
        logger.info("Analyzing sales performance...")
        sales_results = analyzer.sales_performance_analysis()
        
        # Customer Analysis
        logger.info("Analyzing customer behavior...")
        customer_results = analyzer.customer_analysis()
        
        # Product Analysis
        logger.info("Analyzing product performance...")
        product_results = analyzer.product_analysis()
        
        # Channel Analysis
        logger.info("Analyzing sales channels...")
        channel_results = analyzer.channel_analysis()
        
        # Generate Insights
        logger.info("Generating business insights...")
        insights = analyzer.generate_insights()
        
        # Step 4: Display Results
        logger.info("Step 4: Displaying analysis results")
        print("\n" + "="*60)
        print("BUSINESS ANALYTICS DASHBOARD - ANALYSIS RESULTS")
        print("="*60)
        
        # Sales Performance Summary
        print("\n📈 SALES PERFORMANCE SUMMARY")
        print("-" * 40)
        metrics = sales_results['total_metrics']
        print(f"Total Revenue: ${metrics['total_revenue']:,.2f}")
        print(f"Total Transactions: {metrics['total_transactions']:,}")
        print(f"Average Order Value: ${metrics['avg_order_value']:.2f}")
        print(f"Unique Customers: {metrics['unique_customers']:,}")
        print(f"Total Items Sold: {metrics['total_items_sold']:,}")
        
        # Monthly Trend
        monthly_data = sales_results['monthly_trend']
        if not monthly_data.empty and len(monthly_data) > 1:
            latest_month = monthly_data.iloc[-1]
            previous_month = monthly_data.iloc[-2]
            growth_rate = ((latest_month['revenue'] - previous_month['revenue']) / previous_month['revenue']) * 100
            print(f"Latest Month Revenue: ${latest_month['revenue']:,.2f}")
            print(f"Month-over-Month Growth: {growth_rate:+.1f}%")
        
        # Customer Insights
        print("\n👥 CUSTOMER ANALYSIS SUMMARY")
        print("-" * 40)
        segment_data = customer_results['segment_analysis']
        if not segment_data.empty:
            top_segment = segment_data.iloc[0]
            print(f"Most Valuable Segment: {top_segment['customer_segment']}")
            print(f"Average Customer Value: ${top_segment['avg_customer_value']:,.2f}")
            print(f"Customer Count: {top_segment['customer_count']:,}")
        
        # Geographic Distribution
        geo_data = customer_results['geographic_distribution']
        if not geo_data.empty:
            top_state = geo_data.iloc[0]
            print(f"Top State by Revenue: {top_state['state']} (${top_state['total_revenue']:,.2f})")
        
        # Product Performance
        print("\n🛍️ PRODUCT ANALYSIS SUMMARY")
        print("-" * 40)
        category_data = product_results['category_performance']
        if not category_data.empty:
            top_category = category_data.iloc[0]
            print(f"Top Category: {top_category['category']}")
            print(f"Category Revenue: ${top_category['total_revenue']:,.2f}")
            print(f"Total Sales: {top_category['total_sales']:,}")
        
        # Brand Performance
        brand_data = product_results['brand_analysis']
        if not brand_data.empty:
            top_brand = brand_data.iloc[0]
            print(f"Top Brand: {top_brand['brand']} (${top_brand['total_revenue']:,.2f})")
        
        # Channel Performance
        print("\n🚀 CHANNEL ANALYSIS SUMMARY")
        print("-" * 40)
        channel_data = channel_results['channel_performance']
        if not channel_data.empty:
            top_channel = channel_data.iloc[0]
            print(f"Top Sales Channel: {top_channel['sales_channel']}")
            print(f"Channel Revenue: ${top_channel['total_revenue']:,.2f}")
            print(f"Transaction Share: {top_channel['percentage']:.1f}%")
        
        # Payment Methods
        payment_data = channel_results['payment_analysis']
        if not payment_data.empty:
            top_payment = payment_data.iloc[0]
            print(f"Most Used Payment: {top_payment['payment_method']} ({top_payment['usage_percentage']:.1f}%)")
        
        # Business Insights
        print("\n💡 KEY BUSINESS INSIGHTS")
        print("-" * 40)
        for category, insight_list in insights.items():
            if insight_list:
                print(f"\n{category.replace('_', ' ').title()}:")
                for insight in insight_list[:3]:  # Show top 3 insights per category
                    print(f"  • {insight}")
        
        # Step 5: Generate Summary Report
        logger.info("Step 5: Generating summary report")
        
        report_filename = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w') as f:
            f.write("BUSINESS ANALYTICS DASHBOARD - COMPREHENSIVE REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write all analysis results to file
            f.write("SALES PERFORMANCE METRICS\n")
            f.write("-" * 30 + "\n")
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    if 'amount' in key or 'revenue' in key:
                        f.write(f"{key.replace('_', ' ').title()}: ${value:,.2f}\n")
                    else:
                        f.write(f"{key.replace('_', ' ').title()}: {value:,}\n")
                else:
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            
            f.write("\nBUSINESS INSIGHTS\n")
            f.write("-" * 30 + "\n")
            for category, insight_list in insights.items():
                if insight_list:
                    f.write(f"\n{category.replace('_', ' ').title()}:\n")
                    for insight in insight_list:
                        f.write(f"  • {insight}\n")
        
        print(f"\n📄 Detailed report saved to: {report_filename}")
        
        # Step 6: Launch Dashboard
        print("\n🚀 LAUNCH DASHBOARD")
        print("-" * 40)
        print("To launch the interactive dashboard, run:")
        print("streamlit run src/streamlit_app.py")
        print("\nThen open your browser to: http://localhost:8501")
        
        logger.info("Analysis pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Error in analysis pipeline: {e}")
        print(f"\n❌ Error: {e}")
        print("Check the analysis.log file for detailed error information")
        sys.exit(1)

if __name__ == "__main__":
    main()