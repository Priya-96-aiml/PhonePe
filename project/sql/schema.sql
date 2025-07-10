
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS sales_summary;
DROP TABLE IF EXISTS customer_metrics;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    registration_date TEXT,
    customer_segment TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    subcategory TEXT,
    brand TEXT,
    price REAL,
    cost REAL,
    stock_quantity INTEGER
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    transaction_date TEXT,
    quantity INTEGER,
    unit_price REAL,
    total_amount REAL,
    discount_amount REAL,
    payment_method TEXT,
    sales_channel TEXT
);

CREATE TABLE sales_summary (
    summary_date TEXT PRIMARY KEY,
    total_sales REAL,
    total_transactions INTEGER,
    unique_customers INTEGER,
    average_order_value REAL
);

CREATE TABLE customer_metrics (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_segment TEXT,
    total_spent REAL,
    total_transactions INTEGER,
    avg_order_value REAL,
    last_purchase_date TEXT
);
