"""
Data extraction module for loading and processing data from various sources.
This module handles data ingestion, cleaning, and initial processing.
"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import random
from config.database_config import db_config
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExtractor:
    """Handles data extraction and loading operations."""
    
    def __init__(self):
        self.db_config = db_config

    def generate_sample_data(self, num_customers: int = 100, num_products: int = 50, num_transactions: int = 1000) -> Dict[str, pd.DataFrame]:
        logger.info(f"Generating sample data: {num_customers} customers, {num_products} products, {num_transactions} transactions")

        customers_data = []
        customer_segments = ['Premium', 'Standard', 'Basic']
        states = ['NY', 'CA', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']

        for i in range(1, num_customers + 1):
            customers_data.append({
                'customer_id': i,
                'first_name': f'Customer{i}',
                'last_name': f'Last{i}',
                'email': f'customer{i}@email.com',
                'phone': f'555-{i:04d}',
                'address': f'{i} Main St',
                'city': f'City{i % 20}',
                'state': random.choice(states),
                'zip_code': f'{10000 + i:05d}',
                'registration_date': datetime.now() - timedelta(days=random.randint(30, 365)),
                'customer_segment': random.choice(customer_segments)
            })

        customers_df = pd.DataFrame(customers_data)

        categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
        brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']

        products_data = []
        for i in range(1, num_products + 1):
            cost = random.uniform(10, 200)
            price = cost * random.uniform(1.5, 3.0)

            products_data.append({
                'product_id': i,
                'product_name': f'Product {i}',
                'category': random.choice(categories),
                'subcategory': f'Sub{i % 10}',
                'brand': random.choice(brands),
                'price': round(price, 2),
                'cost': round(cost, 2),
                'stock_quantity': random.randint(10, 200)
            })

        products_df = pd.DataFrame(products_data)

        payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'PayPal']
        sales_channels = ['Online', 'In-Store', 'Mobile App']

        transactions_data = []
        for i in range(1, num_transactions + 1):
            customer_id = random.randint(1, num_customers)
            product_id = random.randint(1, num_products)
            product_price = products_df[products_df['product_id'] == product_id]['price'].iloc[0]
            quantity = random.randint(1, 5)
            discount = random.uniform(0, product_price * 0.2) if random.random() < 0.3 else 0

            transactions_data.append({
                'transaction_id': i,
                'customer_id': customer_id,
                'product_id': product_id,
                'transaction_date': datetime.now() - timedelta(days=random.randint(1, 90)),
                'quantity': quantity,
                'unit_price': product_price,
                'total_amount': round((product_price * quantity) - discount, 2),
                'discount_amount': round(discount, 2),
                'payment_method': random.choice(payment_methods),
                'sales_channel': random.choice(sales_channels)
            })

        transactions_df = pd.DataFrame(transactions_data)

        return {
            'customers': customers_df,
            'products': products_df,
            'transactions': transactions_df
        }

    def load_data_to_database(self, dataframes: Dict[str, pd.DataFrame]) -> bool:
        try:
            engine = self.db_config.get_engine()
            for table_name, df in dataframes.items():
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                logger.info(f"Loaded {len(df)} records to {table_name} table")
            self._generate_sales_summary()
            return True
        except Exception as e:
            logger.error(f"Error loading data to database: {e}")
            return False

    def _generate_sales_summary(self):
        query = """
        INSERT OR REPLACE INTO sales_summary (summary_date, total_sales, total_transactions, unique_customers, average_order_value)
        SELECT 
            DATE(transaction_date) as summary_date,
            SUM(total_amount) as total_sales,
            COUNT(transaction_id) as total_transactions,
            COUNT(DISTINCT customer_id) as unique_customers,
            AVG(total_amount) as average_order_value
        FROM transactions
        GROUP BY DATE(transaction_date)
        ORDER BY summary_date;
        """
        with self.db_config.get_connection() as conn:
            conn.execute(query)
            conn.commit()
        logger.info("Generated sales summary data")

    def extract_from_csv(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Extracted {len(df)} records from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            raise

    def validate_data(self, df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate dataframe structure and data quality.
        """
        issues = []

        # Check required columns
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            issues.append(f"Missing columns: {missing_columns}")

        # Check for null values in required columns
        for col in required_columns:
            if col in df.columns and df[col].isnull().any():
                null_count = df[col].isnull().sum()
                issues.append(f"Column '{col}' has {null_count} null values")

        # Validate date format if applicable
        if 'transaction_date' in df.columns:
            try:
                pd.to_datetime(df['transaction_date'])
            except:
                issues.append("Invalid date format in transaction_date column")

        is_valid = len(issues) == 0
        return is_valid, issues

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess data.
        Removes duplicates and rows with missing values.
        """
        cleaned_df = df.copy()
        cleaned_df = cleaned_df.drop_duplicates()
        cleaned_df = cleaned_df.dropna()

        # Strip whitespace from string columns
        text_cols = cleaned_df.select_dtypes(include='object').columns
        for col in text_cols:
            cleaned_df[col] = cleaned_df[col].str.strip()

        return cleaned_df


def main():
    """Main function to demonstrate data extraction."""
    extractor = DataExtractor()

    # Initialize schema
    db_config.execute_script('sql/schema.sql')

    # Generate and load sample data
    sample_data = extractor.generate_sample_data()
    success = extractor.load_data_to_database(sample_data)

    if success:
        logger.info("Data extraction and loading completed successfully")
    else:
        logger.error("Data extraction and loading failed")


if __name__ == "__main__":
    main()
