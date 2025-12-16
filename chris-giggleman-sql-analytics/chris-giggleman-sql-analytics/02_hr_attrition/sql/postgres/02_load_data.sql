\
\copy employees(employee_id,full_name,department,role,location,hire_date,termination_date,salary,performance_rating)
FROM '02_hr_attrition/data/raw/employee_roster.csv' WITH (FORMAT csv, HEADER true);
