-- Data quality checks (SQLite) - expect 0 rows

-- end_date before start_date
SELECT *
FROM subscriptions
WHERE end_date IS NOT NULL
  AND date(end_date) < date(start_date);

-- missing critical fields
SELECT *
FROM subscriptions
WHERE account_id IS NULL OR plan IS NULL OR start_date IS NULL OR monthly_price IS NULL;
