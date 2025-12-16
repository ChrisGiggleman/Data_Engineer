-- Cleaning (SQLite)

UPDATE subscriptions
SET plan = TRIM(plan),
    industry = NULLIF(TRIM(industry), '');

-- Normalize plan values
UPDATE subscriptions SET plan='Basic'    WHERE LOWER(plan)='basic';
UPDATE subscriptions SET plan='Pro'      WHERE LOWER(plan)='pro';
UPDATE subscriptions SET plan='Business' WHERE LOWER(plan) IN ('business','biz');

-- Empty end_date -> NULL
UPDATE subscriptions SET end_date = NULL WHERE end_date = '';

-- Missing seats -> set to 1 (explicit business rule for analytics)
UPDATE subscriptions SET seats = 1 WHERE seats IS NULL OR seats = '';

-- Trim only, keep dates as ISO text
