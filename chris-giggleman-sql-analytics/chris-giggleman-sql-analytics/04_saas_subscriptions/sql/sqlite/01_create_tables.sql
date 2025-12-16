DROP TABLE IF EXISTS subscriptions;

CREATE TABLE subscriptions (
  subscription_id INTEGER PRIMARY KEY,
  account_id      INTEGER NOT NULL,
  plan            TEXT NOT NULL,
  start_date      TEXT NOT NULL,
  end_date        TEXT,
  monthly_price   REAL NOT NULL,
  industry        TEXT,
  seats           INTEGER
);

CREATE INDEX idx_subs_account ON subscriptions(account_id);
CREATE INDEX idx_subs_dates ON subscriptions(start_date, end_date);
