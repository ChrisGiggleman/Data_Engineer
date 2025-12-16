-- Data quality tests (SQLite) - expect 0 rows

-- Hire after termination (invalid)
SELECT *
FROM employees
WHERE termination_date IS NOT NULL
  AND julianday(termination_date) < julianday(hire_date);

-- Missing department/role/location
SELECT *
FROM employees
WHERE department IS NULL OR role IS NULL OR location IS NULL;

-- Ratings out of range (should be prevented by constraint, but good to test)
SELECT *
FROM employees
WHERE performance_rating NOT BETWEEN 1 AND 5;
