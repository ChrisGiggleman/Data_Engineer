-- Cleaning (PostgreSQL)

UPDATE employees
SET department = NULLIF(BTRIM(department), ''),
    role       = NULLIF(BTRIM(role), ''),
    location   = NULLIF(BTRIM(location), '');

-- Normalize department casing (mapping)
UPDATE employees SET department = 'Sales'       WHERE LOWER(department) = 'sales';
UPDATE employees SET department = 'Engineering' WHERE LOWER(department) = 'engineering';
UPDATE employees SET department = 'Support'     WHERE LOWER(department) = 'support';
UPDATE employees SET department = 'Finance'     WHERE LOWER(department) = 'finance';
UPDATE employees SET department = 'Marketing'   WHERE LOWER(department) = 'marketing';

-- Impute missing salary with department median (Postgres has percentile_cont)
WITH med AS (
  SELECT
    department,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
  FROM employees
  WHERE salary IS NOT NULL
  GROUP BY 1
)
UPDATE employees e
SET salary = med.median_salary::INT
FROM med
WHERE e.department = med.department
  AND e.salary IS NULL;

UPDATE employees SET full_name = BTRIM(full_name);
