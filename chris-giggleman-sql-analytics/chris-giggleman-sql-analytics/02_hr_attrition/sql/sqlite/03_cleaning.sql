-- Cleaning (SQLite)

-- Trim and standardize text
UPDATE employees
SET department = TRIM(department),
    role = TRIM(role),
    location = TRIM(location);

-- Normalize department casing (simple mapping)
UPDATE employees SET department = 'Sales'       WHERE LOWER(department) = 'sales';
UPDATE employees SET department = 'Engineering' WHERE LOWER(department) = 'engineering';
UPDATE employees SET department = 'Support'     WHERE LOWER(department) = 'support';
UPDATE employees SET department = 'Finance'     WHERE LOWER(department) = 'finance';
UPDATE employees SET department = 'Marketing'   WHERE LOWER(department) = 'marketing';

-- Convert empty strings to NULL
UPDATE employees SET termination_date = NULL WHERE termination_date = '';
UPDATE employees SET salary = NULL WHERE salary = '';

-- Impute missing salary with department median approximation (fallback to avg)
-- SQLite doesn't have MEDIAN built-in; use AVG by dept as a simple, explainable rule.
UPDATE employees e
SET salary = (
  SELECT CAST(AVG(salary) AS INT)
  FROM employees
  WHERE department = e.department AND salary IS NOT NULL
)
WHERE salary IS NULL;

-- Remove accidental whitespace-only names
UPDATE employees SET full_name = TRIM(full_name);
