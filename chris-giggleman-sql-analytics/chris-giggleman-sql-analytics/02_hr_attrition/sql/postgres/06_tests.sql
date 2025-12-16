-- Data quality tests (PostgreSQL) - expect 0 rows

-- Hire after termination
SELECT *
FROM employees
WHERE termination_date IS NOT NULL
  AND termination_date < hire_date;

-- Missing categories
SELECT *
FROM employees
WHERE department IS NULL OR role IS NULL OR location IS NULL;

-- Ratings out of range
SELECT *
FROM employees
WHERE performance_rating NOT BETWEEN 1 AND 5;
