-- Cleaning steps (SQLite)

-- 1) Trim whitespace
UPDATE customers
SET full_name = TRIM(full_name),
    email = TRIM(email),
    city = TRIM(city),
    state = TRIM(state);

-- 2) Convert empty strings to NULL
UPDATE customers SET full_name = NULL WHERE full_name = '';
UPDATE customers SET email = NULL WHERE email = '';

UPDATE products
SET product_name = TRIM(product_name),
    category = TRIM(category);

UPDATE orders
SET status = TRIM(status),
    channel = TRIM(channel);

-- 3) Fix missing shipping_cost to 0
UPDATE orders
SET shipping_cost = COALESCE(shipping_cost, 0);

-- 4) Infer missing product prices from order_items (if possible)
UPDATE products
SET unit_price = (
  SELECT AVG(oi.unit_price)
  FROM order_items oi
  WHERE oi.product_id = products.product_id
    AND oi.unit_price IS NOT NULL
)
WHERE unit_price IS NULL;

-- 5) Fill missing order item unit_price from products
UPDATE order_items
SET unit_price = COALESCE(unit_price, (SELECT p.unit_price FROM products p WHERE p.product_id = order_items.product_id))
WHERE unit_price IS NULL;

-- 6) Replace NULL discounts with 0
UPDATE order_items
SET discount = COALESCE(discount, 0);
