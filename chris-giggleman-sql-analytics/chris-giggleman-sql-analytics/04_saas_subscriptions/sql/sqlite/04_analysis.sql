-- SaaS analysis (SQLite)
-- SQLite doesn't have generate_series; use a recursive month calendar for the covered range.

-- 1) Build a month calendar from min(start_date) to max(COALESCE(end_date, today))
WITH RECURSIVE bounds AS (
  SELECT
    date(MIN(start_date), 'start of month') AS min_month,
    date(MAX(COALESCE(end_date, date('now'))), 'start of month') AS max_month
  FROM subscriptions
),
months(m) AS (
  SELECT min_month FROM bounds
  UNION ALL
  SELECT date(m, '+1 month')
  FROM months, bounds
  WHERE m < max_month
),
active AS (
  SELECT
    months.m AS month_start,
    s.subscription_id,
    s.account_id,
    s.industry,
    s.monthly_price
  FROM months
  JOIN subscriptions s
    ON date(s.start_date) <= date(months.m, '+1 month', '-1 day')
   AND (s.end_date IS NULL OR date(s.end_date) >= months.m)
)
SELECT
  month_start,
  COUNT(DISTINCT subscription_id) AS active_subs,
  ROUND(SUM(monthly_price),2) AS mrr
FROM active
GROUP BY 1
ORDER BY 1;

-- 2) Churned accounts by month (end_date month)
WITH churn AS (
  SELECT date(end_date, 'start of month') AS churn_month, COUNT(DISTINCT account_id) AS churned_accounts
  FROM subscriptions
  WHERE end_date IS NOT NULL
  GROUP BY 1
)
SELECT churn_month, churned_accounts
FROM churn
ORDER BY churn_month;

-- 3) Churn by industry
SELECT
  industry,
  COUNT(DISTINCT account_id) AS churned_accounts
FROM subscriptions
WHERE end_date IS NOT NULL
GROUP BY 1
ORDER BY churned_accounts DESC;

-- 4) Cohort retention (accounts)
WITH cohorts AS (
  SELECT account_id, date(MIN(start_date), 'start of month') AS cohort_month
  FROM subscriptions
  GROUP BY 1
),
calendar AS (
  WITH RECURSIVE months(m) AS (
    SELECT date((SELECT MIN(cohort_month) FROM cohorts))
    UNION ALL
    SELECT date(m, '+1 month') FROM months
    WHERE m < date('now', 'start of month')
  )
  SELECT m FROM months
),
active_accounts AS (
  SELECT
    c.cohort_month,
    cal.m AS month_start,
    COUNT(DISTINCT s.account_id) AS active_accounts
  FROM cohorts c
  JOIN calendar cal
  LEFT JOIN subscriptions s
    ON s.account_id = c.account_id
   AND date(s.start_date) <= date(cal.m, '+1 month', '-1 day')
   AND (s.end_date IS NULL OR date(s.end_date) >= cal.m)
  WHERE cal.m >= c.cohort_month
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
