-- Basic data quality checks (SQLite)
-- Expect 0 rows returned for each "bad" check.

-- 1) Orphan order_items
SELECT oi.*
FROM order_items oi
LEFT JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_id IS NULL;

-- 2) Negative pricing after discounts
SELECT *
FROM order_items
WHERE (unit_price - discount) < 0;

-- 3) Missing critical fields
SELECT *
FROM orders
WHERE order_date IS NULL OR status IS NULL OR channel IS NULL;
