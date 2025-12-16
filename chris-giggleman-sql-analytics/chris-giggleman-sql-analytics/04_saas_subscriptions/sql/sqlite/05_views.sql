-- Views (SQLite)
DROP VIEW IF EXISTS v_subscriptions_clean;

CREATE VIEW v_subscriptions_clean AS
SELECT
  subscription_id,
  account_id,
  plan,
  date(start_date) AS start_date,
  CASE WHEN end_date IS NULL THEN NULL ELSE date(end_date) END AS end_date,
  monthly_price,
  industry,
  seats
FROM subscriptions;
