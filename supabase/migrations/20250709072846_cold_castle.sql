-- Sample data insertion for testing and demonstration
-- This script populates the database with realistic sample data

-- Insert sample customers
INSERT INTO customers (customer_id, first_name, last_name, email, phone, address, city, state, zip_code, registration_date, customer_segment) VALUES
(1, 'John', 'Smith', 'john.smith@email.com', '555-0101', '123 Main St', 'New York', 'NY', '10001', '2023-01-15', 'Premium'),
(2, 'Sarah', 'Johnson', 'sarah.j@email.com', '555-0102', '456 Oak Ave', 'Los Angeles', 'CA', '90210', '2023-02-20', 'Standard'),
(3, 'Michael', 'Brown', 'mike.brown@email.com', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60601', '2023-03-10', 'Basic'),
(4, 'Emily', 'Davis', 'emily.davis@email.com', '555-0104', '321 Elm St', 'Houston', 'TX', '77001', '2023-01-25', 'Premium'),
(5, 'David', 'Wilson', 'david.w@email.com', '555-0105', '654 Maple Dr', 'Phoenix', 'AZ', '85001', '2023-04-05', 'Standard'),
(6, 'Lisa', 'Anderson', 'lisa.anderson@email.com', '555-0106', '987 Cedar Ln', 'Philadelphia', 'PA', '19101', '2023-02-14', 'Basic'),
(7, 'Robert', 'Taylor', 'robert.t@email.com', '555-0107', '147 Birch St', 'San Antonio', 'TX', '78201', '2023-03-22', 'Premium'),
(8, 'Jennifer', 'Martinez', 'jen.martinez@email.com', '555-0108', '258 Spruce Ave', 'San Diego', 'CA', '92101', '2023-01-30', 'Standard'),
(9, 'William', 'Garcia', 'will.garcia@email.com', '555-0109', '369 Fir Rd', 'Dallas', 'TX', '75201', '2023-04-12', 'Basic'),
(10, 'Amanda', 'Rodriguez', 'amanda.r@email.com', '555-0110', '741 Ash Dr', 'San Jose', 'CA', '95101', '2023-02-28', 'Premium');

-- Insert sample products
INSERT INTO products (product_id, product_name, category, subcategory, brand, price, cost, stock_quantity) VALUES
(1, 'Wireless Headphones', 'Electronics', 'Audio', 'TechBrand', 199.99, 120.00, 50),
(2, 'Smartphone Case', 'Electronics', 'Accessories', 'ProtectPro', 29.99, 15.00, 200),
(3, 'Bluetooth Speaker', 'Electronics', 'Audio', 'SoundMax', 89.99, 55.00, 75),
(4, 'Laptop Stand', 'Electronics', 'Accessories', 'ErgoTech', 79.99, 45.00, 30),
(5, 'USB-C Cable', 'Electronics', 'Cables', 'ConnectPlus', 19.99, 8.00, 150),
(6, 'Wireless Mouse', 'Electronics', 'Computer', 'ClickMaster', 49.99, 25.00, 100),
(7, 'Keyboard', 'Electronics', 'Computer', 'TypePro', 129.99, 70.00, 40),
(8, 'Monitor', 'Electronics', 'Computer', 'ViewMax', 299.99, 180.00, 25),
(9, 'Webcam', 'Electronics', 'Computer', 'ClearView', 69.99, 35.00, 60),
(10, 'Power Bank', 'Electronics', 'Accessories', 'PowerPlus', 39.99, 20.00, 80);

-- Insert sample transactions
INSERT INTO transactions (transaction_id, customer_id, product_id, transaction_date, quantity, unit_price, total_amount, discount_amount, payment_method, sales_channel) VALUES
(1, 1, 1, '2023-05-01', 1, 199.99, 199.99, 0.00, 'Credit Card', 'Online'),
(2, 2, 2, '2023-05-02', 2, 29.99, 59.98, 5.00, 'PayPal', 'Online'),
(3, 3, 3, '2023-05-03', 1, 89.99, 89.99, 0.00, 'Debit Card', 'In-Store'),
(4, 1, 4, '2023-05-04', 1, 79.99, 79.99, 10.00, 'Credit Card', 'Online'),
(5, 4, 5, '2023-05-05', 3, 19.99, 59.97, 0.00, 'Credit Card', 'Mobile App'),
(6, 5, 6, '2023-05-06', 1, 49.99, 49.99, 0.00, 'Debit Card', 'In-Store'),
(7, 2, 7, '2023-05-07', 1, 129.99, 129.99, 15.00, 'PayPal', 'Online'),
(8, 6, 8, '2023-05-08', 1, 299.99, 299.99, 30.00, 'Credit Card', 'Online'),
(9, 7, 9, '2023-05-09', 1, 69.99, 69.99, 0.00, 'Credit Card', 'Mobile App'),
(10, 3, 10, '2023-05-10', 2, 39.99, 79.98, 8.00, 'Cash', 'In-Store'),
(11, 8, 1, '2023-05-11', 1, 199.99, 199.99, 20.00, 'Debit Card', 'Online'),
(12, 9, 2, '2023-05-12', 1, 29.99, 29.99, 0.00, 'PayPal', 'Mobile App'),
(13, 10, 3, '2023-05-13', 1, 89.99, 89.99, 0.00, 'Credit Card', 'Online'),
(14, 4, 6, '2023-05-14', 2, 49.99, 99.98, 10.00, 'Credit Card', 'In-Store'),
(15, 1, 8, '2023-05-15', 1, 299.99, 299.99, 0.00, 'Credit Card', 'Online');

-- Insert sample sales summary data
INSERT INTO sales_summary (summary_date, total_sales, total_transactions, unique_customers, average_order_value) VALUES
('2023-05-01', 199.99, 1, 1, 199.99),
('2023-05-02', 54.98, 1, 1, 54.98),
('2023-05-03', 89.99, 1, 1, 89.99),
('2023-05-04', 69.99, 1, 1, 69.99),
('2023-05-05', 59.97, 1, 1, 59.97),
('2023-05-06', 49.99, 1, 1, 49.99),
('2023-05-07', 114.99, 1, 1, 114.99),
('2023-05-08', 269.99, 1, 1, 269.99),
('2023-05-09', 69.99, 1, 1, 69.99),
('2023-05-10', 71.98, 1, 1, 71.98);