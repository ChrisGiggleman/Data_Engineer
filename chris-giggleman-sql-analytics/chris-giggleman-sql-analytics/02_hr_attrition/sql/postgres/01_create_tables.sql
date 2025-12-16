DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
  employee_id        INT PRIMARY KEY,
  full_name          TEXT NOT NULL,
  department         TEXT,
  role               TEXT,
  location           TEXT,
  hire_date          DATE NOT NULL,
  termination_date   DATE,
  salary             INT,
  performance_rating INT CHECK (performance_rating BETWEEN 1 AND 5)
);

CREATE INDEX idx_employees_dept ON employees(department);
CREATE INDEX idx_employees_loc ON employees(location);
