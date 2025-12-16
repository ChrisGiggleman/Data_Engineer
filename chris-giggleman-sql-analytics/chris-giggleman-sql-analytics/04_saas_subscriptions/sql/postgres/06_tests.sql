-- Data quality checks (PostgreSQL) - expect 0 rows

SELECT *
FROM subscriptions
WHERE end_date IS NOT NULL AND end_date < start_date;

SELECT *
FROM subscriptions
WHERE account_id IS NULL OR plan IS NULL OR start_date IS NULL OR monthly_price IS NULL;
