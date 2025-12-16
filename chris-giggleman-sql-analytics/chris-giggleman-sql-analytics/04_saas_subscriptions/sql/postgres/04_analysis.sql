-- SaaS analysis (PostgreSQL)

-- Month calendar
WITH bounds AS (
  SELECT
    date_trunc('month', MIN(start_date))::date AS min_month,
    date_trunc('month', MAX(COALESCE(end_date, CURRENT_DATE)))::date AS max_month
  FROM subscriptions
),
months AS (
  SELECT generate_series(min_month, max_month, interval '1 month')::date AS month_start
  FROM bounds
),
active AS (
  SELECT
    m.month_start,
    s.subscription_id,
    s.account_id,
    s.industry,
    s.monthly_price
  FROM months m
  JOIN subscriptions s
    ON s.start_date <= (m.month_start + interval '1 month' - interval '1 day')
   AND (s.end_date IS NULL OR s.end_date >= m.month_start)
)
SELECT
  month_start,
  COUNT(DISTINCT subscription_id) AS active_subs,
  ROUND(SUM(monthly_price),2) AS mrr
FROM active
GROUP BY 1
ORDER BY 1;

-- Churned accounts by month
SELECT
  date_trunc('month', end_date)::date AS churn_month,
  COUNT(DISTINCT account_id) AS churned_accounts
FROM subscriptions
WHERE end_date IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- Churn by industry
SELECT
  industry,
  COUNT(DISTINCT account_id) AS churned_accounts
FROM subscriptions
WHERE end_date IS NOT NULL
GROUP BY 1
ORDER BY churned_accounts DESC;

-- Cohort retention (accounts)
WITH cohorts AS (
  SELECT account_id, date_trunc('month', MIN(start_date))::date AS cohort_month
  FROM subscriptions
  GROUP BY 1
),
months AS (
  SELECT generate_series(
    (SELECT MIN(cohort_month) FROM cohorts),
    date_trunc('month', CURRENT_DATE)::date,
    interval '1 month'
  )::date AS month_start
),
active_accounts AS (
  SELECT
    c.cohort_month,
    m.month_start,
    COUNT(DISTINCT s.account_id) AS active_accounts
  FROM cohorts c
  JOIN months m ON m.month_start >= c.cohort_month
  LEFT JOIN subscriptions s
    ON s.account_id = c.account_id
   AND s.start_date <= (m.month_start + interval '1 month' - interval '1 day')
   AND (s.end_date IS NULL OR s.end_date >= m.month_start)
  GROUP BY 1,2
),
cohort_size AS (
  SELECT cohort_month, COUNT(*) AS cohort_accounts
  FROM cohorts
  GROUP BY 1
)
SELECT
  a.cohort_month,
  a.month_start,
  a.active_accounts,
  cs.cohort_accounts,
  ROUND(100.0 * a.active_accounts / cs.cohort_accounts, 2) AS retention_pct
FROM active_accounts a
JOIN cohort_size cs ON cs.cohort_month = a.cohort_month
ORDER BY a.cohort_month, a.month_start;
