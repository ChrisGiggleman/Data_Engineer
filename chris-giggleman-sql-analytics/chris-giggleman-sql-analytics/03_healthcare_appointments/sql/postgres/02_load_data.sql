\
\copy appointments(appointment_id,patient_id,clinic,provider,booked_at,appointment_at,status,insurance_type)
FROM '03_healthcare_appointments/data/raw/appointments.csv' WITH (FORMAT csv, HEADER true);
