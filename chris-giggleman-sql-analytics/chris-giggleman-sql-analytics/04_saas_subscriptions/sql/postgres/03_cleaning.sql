UPDATE subscriptions
SET plan = BTRIM(plan),
    industry = NULLIF(BTRIM(industry), ''),
    seats = COALESCE(seats, 1);

UPDATE subscriptions SET plan='Basic'    WHERE LOWER(plan)='basic';
UPDATE subscriptions SET plan='Pro'      WHERE LOWER(plan)='pro';
UPDATE subscriptions SET plan='Business' WHERE LOWER(plan) IN ('business','biz');
