PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

CREATE TABLE customers (
  customer_id   INTEGER PRIMARY KEY,
  full_name     TEXT,
  email         TEXT,
  city          TEXT,
  state         TEXT,
  created_at    TEXT  -- ISO date
);

CREATE TABLE products (
  product_id    INTEGER PRIMARY KEY,
  product_name  TEXT NOT NULL,
  category      TEXT NOT NULL,
  unit_price    REAL,
  active        INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE orders (
  order_id      INTEGER PRIMARY KEY,
  customer_id   INTEGER NOT NULL,
  order_date    TEXT NOT NULL,
  status        TEXT NOT NULL,
  channel       TEXT NOT NULL,
  shipping_cost REAL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
  order_item_id INTEGER PRIMARY KEY,
  order_id      INTEGER NOT NULL,
  product_id    INTEGER NOT NULL,
  quantity      INTEGER NOT NULL CHECK (quantity > 0),
  unit_price    REAL,
  discount      REAL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
