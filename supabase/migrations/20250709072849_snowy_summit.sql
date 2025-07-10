-- Advanced SQL queries for data analysis
-- These queries provide insights into sales performance, customer behavior, and product trends

-- 1. Top 10 customers by total spending
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.customer_segment,
    SUM(t.total_amount) as total_spent,
    COUNT(t.transaction_id) as total_orders,
    AVG(t.total_amount) as avg_order_value
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.customer_segment
ORDER BY total_spent DESC
LIMIT 10;

-- 2. Monthly sales trend analysis
SELECT 
    strftime('%Y-%m', transaction_date) as month,
    COUNT(transaction_id) as total_transactions,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(quantity) as total_items_sold
FROM transactions
GROUP BY strftime('%Y-%m', transaction_date)
ORDER BY month;

-- 3. Product category performance
SELECT 
    p.category,
    COUNT(t.transaction_id) as total_sales,
    SUM(t.total_amount) as total_revenue,
    AVG(t.total_amount) as avg_sale_amount,
    SUM(t.quantity) as total_quantity_sold,
    COUNT(DISTINCT t.customer_id) as unique_customers
FROM products p
JOIN transactions t ON p.product_id = t.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 4. Customer segmentation analysis
SELECT 
    customer_segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_customer_value,
    AVG(total_transactions) as avg_transactions_per_customer,
    AVG(avg_order_value) as avg_order_value
FROM customer_metrics
GROUP BY customer_segment
ORDER BY avg_customer_value DESC;

-- 5. Sales channel performance
SELECT 
    sales_channel,
    COUNT(transaction_id) as total_transactions,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT customer_id) as unique_customers,
    ROUND(COUNT(transaction_id) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as percentage_of_total
FROM transactions
GROUP BY sales_channel
ORDER BY total_revenue DESC;

-- 6. Payment method analysis
SELECT 
    payment_method,
    COUNT(transaction_id) as transaction_count,
    SUM(total_amount) as total_amount,
    AVG(total_amount) as avg_transaction_value,
    ROUND(COUNT(transaction_id) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as usage_percentage
FROM transactions
GROUP BY payment_method
ORDER BY transaction_count DESC;

-- 7. Top performing products
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
GROUP BY p.product_id, p.product_name, p.category, p.brand, p.price, p.cost
ORDER BY total_revenue DESC
LIMIT 10;

-- 8. Customer retention analysis
WITH customer_purchase_months AS (
    SELECT 
        customer_id,
        strftime('%Y-%m', transaction_date) as purchase_month,
        COUNT(transaction_id) as monthly_transactions
    FROM transactions
    GROUP BY customer_id, strftime('%Y-%m', transaction_date)
),
customer_activity AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT purchase_month) as active_months,
        MIN(purchase_month) as first_purchase_month,
        MAX(purchase_month) as last_purchase_month
    FROM customer_purchase_months
    GROUP BY customer_id
)
SELECT 
    active_months,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT customer_id) FROM transactions), 2) as percentage
FROM customer_activity
GROUP BY active_months
ORDER BY active_months;

-- 9. Discount impact analysis
SELECT 
    CASE 
        WHEN discount_amount = 0 THEN 'No Discount'
        WHEN discount_amount <= 10 THEN 'Low Discount (≤$10)'
        WHEN discount_amount <= 25 THEN 'Medium Discount ($11-$25)'
        ELSE 'High Discount (>$25)'
    END as discount_category,
    COUNT(transaction_id) as transaction_count,
    AVG(total_amount) as avg_order_value,
    AVG(quantity) as avg_items_per_order,
    SUM(total_amount) as total_revenue
FROM transactions
GROUP BY discount_category
ORDER BY avg_order_value DESC;

-- 10. Geographic sales distribution
SELECT 
    c.state,
    COUNT(DISTINCT c.customer_id) as customer_count,
    COUNT(t.transaction_id) as total_transactions,
    SUM(t.total_amount) as total_revenue,
    AVG(t.total_amount) as avg_order_value
FROM customers c
JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.state
ORDER BY total_revenue DESC;