DROP TABLE IF EXISTS subscriptions;

CREATE TABLE subscriptions (
  subscription_id INT PRIMARY KEY,
  account_id      INT NOT NULL,
  plan            TEXT NOT NULL,
  start_date      DATE NOT NULL,
  end_date        DATE,
  monthly_price   NUMERIC(10,2) NOT NULL,
  industry        TEXT,
  seats           INT
);

CREATE INDEX idx_subs_account ON subscriptions(account_id);
CREATE INDEX idx_subs_dates ON subscriptions(start_date, end_date);
