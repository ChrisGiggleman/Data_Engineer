-- Data quality checks (PostgreSQL)
-- Expect 0 rows for each "bad" query.

-- Orphan order_items
SELECT oi.*
FROM order_items oi
LEFT JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_id IS NULL;

-- Negative net price
SELECT *
FROM order_items
WHERE (unit_price - discount) < 0;

-- Missing critical fields
SELECT *
FROM orders
WHERE order_date IS NULL OR status IS NULL OR channel IS NULL;
