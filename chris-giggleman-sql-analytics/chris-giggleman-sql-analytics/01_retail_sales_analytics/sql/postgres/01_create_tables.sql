DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;

CREATE TABLE customers (
  customer_id   INT PRIMARY KEY,
  full_name     TEXT,
  email         TEXT,
  city          TEXT,
  state         TEXT,
  created_at    DATE
);

CREATE TABLE products (
  product_id    INT PRIMARY KEY,
  product_name  TEXT NOT NULL,
  category      TEXT NOT NULL,
  unit_price    NUMERIC(10,2),
  active        BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE orders (
  order_id      INT PRIMARY KEY,
  customer_id   INT NOT NULL REFERENCES customers(customer_id),
  order_date    DATE NOT NULL,
  status        TEXT NOT NULL,
  channel       TEXT NOT NULL,
  shipping_cost NUMERIC(10,2)
);

CREATE TABLE order_items (
  order_item_id INT PRIMARY KEY,
  order_id      INT NOT NULL REFERENCES orders(order_id),
  product_id    INT NOT NULL REFERENCES products(product_id),
  quantity      INT NOT NULL CHECK (quantity > 0),
  unit_price    NUMERIC(10,2),
  discount      NUMERIC(10,2)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
