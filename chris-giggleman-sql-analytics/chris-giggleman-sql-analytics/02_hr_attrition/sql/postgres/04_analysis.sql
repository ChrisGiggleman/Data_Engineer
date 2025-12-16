-- HR analytics (PostgreSQL)

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

-- Tenure days for terminated employees
SELECT
  employee_id,
  full_name,
  department,
  location,
  (termination_date - hire_date) AS tenure_days,
  salary,
  performance_rating
FROM employees
WHERE termination_date IS NOT NULL
ORDER BY tenure_days ASC;

-- Pay equity: median salary by role/location
SELECT
  role,
  location,
  COUNT(*) AS n,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary),0) AS median_salary
FROM employees
GROUP BY 1,2
ORDER BY role, location;

-- Salary outliers (z-score using stddev)
WITH stats AS (
  SELECT department, AVG(salary) AS avg_salary, STDDEV_SAMP(salary) AS sd_salary
  FROM employees
  WHERE salary IS NOT NULL
  GROUP BY 1
)
SELECT e.*,
       ROUND(s.avg_salary,0) AS dept_avg,
       ROUND(s.sd_salary,0) AS dept_sd,
       ROUND((e.salary - s.avg_salary) / NULLIF(s.sd_salary,0), 2) AS z_score
FROM employees e
JOIN stats s ON s.department = e.department
WHERE s.sd_salary IS NOT NULL
  AND (e.salary - s.avg_salary) / s.sd_salary > 2
ORDER BY z_score DESC;
