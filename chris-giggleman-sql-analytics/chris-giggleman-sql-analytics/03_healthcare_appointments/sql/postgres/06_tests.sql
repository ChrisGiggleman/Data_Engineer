-- Data quality checks (PostgreSQL) - expect 0 rows

SELECT *
FROM appointments
WHERE appointment_at < booked_at;

SELECT *
FROM appointments
WHERE clinic IS NULL OR booked_at IS NULL OR appointment_at IS NULL OR status IS NULL;
