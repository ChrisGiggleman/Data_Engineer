-- Cleaning steps (PostgreSQL)

-- 1) Trim whitespace
UPDATE customers
SET full_name = NULLIF(BTRIM(full_name), ''),
    email     = NULLIF(BTRIM(email), ''),
    city      = NULLIF(BTRIM(city), ''),
    state     = NULLIF(BTRIM(state), '');

UPDATE products
SET product_name = BTRIM(product_name),
    category     = BTRIM(category);

UPDATE orders
SET status  = BTRIM(status),
    channel = BTRIM(channel),
    shipping_cost = COALESCE(shipping_cost, 0);

-- 2) Infer missing product prices from order_items
UPDATE products p
SET unit_price = sub.avg_price
FROM (
  SELECT product_id, AVG(unit_price) AS avg_price
  FROM order_items
  WHERE unit_price IS NOT NULL
  GROUP BY 1
) sub
WHERE p.product_id = sub.product_id
  AND p.unit_price IS NULL;

-- 3) Fill missing order item price from products, discounts to 0
UPDATE order_items oi
SET unit_price = COALESCE(oi.unit_price, p.unit_price),
    discount   = COALESCE(oi.discount, 0)
FROM products p
WHERE oi.product_id = p.product_id
  AND (oi.unit_price IS NULL OR oi.discount IS NULL);
