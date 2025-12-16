\
\copy subscriptions(subscription_id,account_id,plan,start_date,end_date,monthly_price,industry,seats)
FROM '04_saas_subscriptions/data/raw/subscriptions.csv' WITH (FORMAT csv, HEADER true);
