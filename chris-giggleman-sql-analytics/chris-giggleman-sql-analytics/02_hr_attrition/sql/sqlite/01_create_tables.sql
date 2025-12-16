DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
  employee_id        INTEGER PRIMARY KEY,
  full_name          TEXT NOT NULL,
  department         TEXT,
  role               TEXT,
  location           TEXT,
  hire_date          TEXT NOT NULL,
  termination_date   TEXT,
  salary             INTEGER,
  performance_rating INTEGER CHECK (performance_rating BETWEEN 1 AND 5)
);

CREATE INDEX idx_employees_dept ON employees(department);
CREATE INDEX idx_employees_loc ON employees(location);
