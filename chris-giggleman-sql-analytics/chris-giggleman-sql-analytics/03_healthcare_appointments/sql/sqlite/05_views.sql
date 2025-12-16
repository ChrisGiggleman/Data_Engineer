DROP VIEW IF EXISTS v_appointments_enriched;

CREATE VIEW v_appointments_enriched AS
SELECT
  *,
  ROUND(julianday(appointment_at) - julianday(booked_at), 0) AS lead_time_days
FROM appointments;
