-- HR analytics (SQLite)

-- Attrition by department
WITH base AS (
  SELECT
    department,
    COUNT(*) AS headcount,
    SUM(CASE WHEN termination_date IS NOT NULL THEN 1 ELSE 0 END) AS terminated
  FROM employees
  GROUP BY 1
)
SELECT
  department,
  headcount,
  terminated,
  ROUND(100.0 * terminated / headcount, 2) AS attrition_pct
FROM base
ORDER BY attrition_pct DESC;

-- Attrition by location
WITH base AS (
  SELECT
    location,
    COUNT(*) AS headcount,
    SUM(CASE WHEN termination_date IS NOT NULL THEN 1 ELSE 0 END) AS terminated
  FROM employees
  GROUP BY 1
)
SELECT
  location,
  headcount,
  terminated,
  ROUND(100.0 * terminated / headcount, 2) AS attrition_pct
FROM base
ORDER BY attrition_pct DESC;

-- Tenure (days) for terminated employees
SELECT
  employee_id,
  full_name,
  department,
  location,
  ROUND(julianday(termination_date) - julianday(hire_date), 0) AS tenure_days,
  salary,
  performance_rating
FROM employees
WHERE termination_date IS NOT NULL
ORDER BY tenure_days ASC;

-- Pay equity: avg salary by role + location
SELECT
  role,
  location,
  COUNT(*) AS n,
  ROUND(AVG(salary),0) AS avg_salary
FROM employees
GROUP BY 1,2
HAVING COUNT(*) >= 1
ORDER BY role, location;

-- Simple salary outliers within department (z-ish via avg +/- 2*stddev approximation)
-- SQLite lacks STDDEV by default; we show an explainable heuristic: > 1.8x dept avg.
WITH dept_avg AS (
  SELECT department, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY 1
)
SELECT e.*,
       ROUND(d.avg_salary,0) AS dept_avg_salary
FROM employees e
JOIN dept_avg d ON d.department = e.department
WHERE e.salary > (1.8 * d.avg_salary)
ORDER BY e.salary DESC;
