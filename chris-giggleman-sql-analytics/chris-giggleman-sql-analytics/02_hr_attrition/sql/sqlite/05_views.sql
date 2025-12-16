DROP VIEW IF EXISTS v_employee_status;

CREATE VIEW v_employee_status AS
SELECT
  employee_id,
  full_name,
  department,
  role,
  location,
  hire_date,
  termination_date,
  CASE WHEN termination_date IS NULL THEN 'Active' ELSE 'Terminated' END AS employment_status,
  salary,
  performance_rating
FROM employees;
