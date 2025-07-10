-- Database schema for analytics project
-- Creates tables for sales, customers, products, and transactions

-- Drop existing tables if they exist
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sales_summary;

-- Create customers table
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

-- Create products table
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

-- Create transactions table
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

-- Create sales summary table for aggregated data
CREATE TABLE sales_summary (
    summary_id INTEGER PRIMARY KEY,
    summary_date DATE NOT NULL,
    total_sales DECIMAL(12, 2) NOT NULL,
    total_transactions INTEGER NOT NULL,
    unique_customers INTEGER NOT NULL,
    average_order_value DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_product ON transactions(product_id);
CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_sales_summary_date ON sales_summary(summary_date);

-- Create views for common queries
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

CREATE VIEW monthly_sales_trend AS
SELECT 
    strftime('%Y-%m', transaction_date) as month,
    COUNT(transaction_id) as total_transactions,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers
FROM transactions
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY month;