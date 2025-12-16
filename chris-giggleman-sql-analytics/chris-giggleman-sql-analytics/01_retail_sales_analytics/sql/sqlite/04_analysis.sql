-- Retail analysis (SQLite)

-- Base order totals (exclude Canceled/Returned for revenue KPIs)
WITH order_totals AS (
  SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    SUM(oi.quantity * (oi.unit_price - oi.discount)) AS item_revenue,
    o.shipping_cost
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  GROUP BY 1,2,3,4, o.shipping_cost
)
SELECT
  COUNT(*) AS orders,
  ROUND(AVG(item_revenue + shipping_cost),2) AS avg_order_value,
  ROUND(SUM(item_revenue + shipping_cost),2) AS total_revenue
FROM order_totals
WHERE status NOT IN ('Returned','Canceled');

-- Revenue by channel
WITH order_totals AS (
  SELECT
    o.channel,
    o.status,
    SUM(oi.quantity * (oi.unit_price - oi.discount) + o.shipping_cost) AS revenue
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  GROUP BY 1,2
)
SELECT channel, ROUND(SUM(revenue),2) AS revenue
FROM order_totals
WHERE status NOT IN ('Returned','Canceled')
GROUP BY 1
ORDER BY revenue DESC;

-- Top products by revenue
SELECT
  p.category,
  p.product_name,
  ROUND(SUM(oi.quantity * (oi.unit_price - oi.discount)),2) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status NOT IN ('Returned','Canceled')
GROUP BY 1,2
ORDER BY revenue DESC
LIMIT 10;

-- Running revenue over time (window function)
WITH daily AS (
  SELECT
    o.order_date,
    SUM(oi.quantity * (oi.unit_price - oi.discount) + o.shipping_cost) AS revenue
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  WHERE o.status NOT IN ('Returned','Canceled')
  GROUP BY o.order_date
)
SELECT
  order_date,
  ROUND(revenue,2) AS revenue,
  ROUND(SUM(revenue) OVER (ORDER BY order_date),2) AS running_revenue
FROM daily
ORDER BY order_date;

-- Repeat customer rate
WITH nonreturn_orders AS (
  SELECT customer_id, order_id
  FROM orders
  WHERE status NOT IN ('Returned','Canceled')
),
cust_counts AS (
  SELECT customer_id, COUNT(*) AS orders
  FROM nonreturn_orders
  GROUP BY 1
)
SELECT
  ROUND(100.0 * SUM(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) / COUNT(*),2) AS repeat_customer_pct
FROM cust_counts;

-- RFM scoring (simple: quintiles via NTILE)
WITH order_totals AS (
  SELECT
    o.customer_id,
    o.order_date,
    SUM(oi.quantity * (oi.unit_price - oi.discount) + o.shipping_cost) AS revenue
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.order_id
  WHERE o.status NOT IN ('Returned','Canceled')
  GROUP BY 1,2
),
rfm AS (
  SELECT
    customer_id,
    MAX(order_date) AS last_order_date,
    COUNT(*) AS frequency,
    SUM(revenue) AS monetary
  FROM order_totals
  GROUP BY 1
),
scored AS (
  SELECT
    customer_id,
    last_order_date,
    frequency,
    monetary,
    NTILE(5) OVER (ORDER BY last_order_date DESC) AS r_score,
    NTILE(5) OVER (ORDER BY frequency) AS f_score,
    NTILE(5) OVER (ORDER BY monetary) AS m_score
  FROM rfm
)
SELECT
  customer_id,
  last_order_date,
  frequency,
  ROUND(monetary,2) AS monetary,
  r_score, f_score, m_score,
  (r_score || f_score || m_score) AS rfm_segment
FROM scored
ORDER BY monetary DESC;
