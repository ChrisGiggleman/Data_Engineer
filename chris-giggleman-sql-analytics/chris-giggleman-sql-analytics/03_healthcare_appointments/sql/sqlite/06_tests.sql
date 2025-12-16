-- Data quality checks (SQLite) - expect 0 rows

-- Appointment before booking (invalid)
SELECT *
FROM appointments
WHERE julianday(appointment_at) < julianday(booked_at);

-- Missing critical fields
SELECT *
FROM appointments
WHERE clinic IS NULL OR booked_at IS NULL OR appointment_at IS NULL OR status IS NULL;
