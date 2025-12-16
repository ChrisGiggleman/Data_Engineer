DROP VIEW IF EXISTS v_subscriptions_clean;

CREATE VIEW v_subscriptions_clean AS
SELECT
  subscription_id,
  account_id,
  plan,
  start_date,
  end_date,
  monthly_price,
  industry,
  seats
FROM subscriptions;
