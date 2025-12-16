-- Views to make analysis reusable (SQLite)

DROP VIEW IF EXISTS v_order_totals;

CREATE VIEW v_order_totals AS
SELECT
  o.order_id,
  o.customer_id,
  o.order_date,
  o.status,
  o.channel,
  SUM(oi.quantity * (oi.unit_price - oi.discount)) AS item_revenue,
  o.shipping_cost,
  SUM(oi.quantity * (oi.unit_price - oi.discount)) + o.shipping_cost AS gross_revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY 1,2,3,4,5, o.shipping_cost;
