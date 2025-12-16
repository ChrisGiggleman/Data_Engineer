\
-- Load CSVs using psql from the project root.
-- Example:
-- \i 01_retail_sales_analytics/sql/postgres/01_create_tables.sql
-- \i 01_retail_sales_analytics/sql/postgres/02_load_data.sql

\copy customers(customer_id,full_name,email,city,state,created_at)
FROM '01_retail_sales_analytics/data/raw/customers.csv' WITH (FORMAT csv, HEADER true);

\copy products(product_id,product_name,category,unit_price,active)
FROM '01_retail_sales_analytics/data/raw/products.csv' WITH (FORMAT csv, HEADER true);

\copy orders(order_id,customer_id,order_date,status,channel,shipping_cost)
FROM '01_retail_sales_analytics/data/raw/orders.csv' WITH (FORMAT csv, HEADER true);

\copy order_items(order_item_id,order_id,product_id,quantity,unit_price,discount)
FROM '01_retail_sales_analytics/data/raw/order_items.csv' WITH (FORMAT csv, HEADER true);
