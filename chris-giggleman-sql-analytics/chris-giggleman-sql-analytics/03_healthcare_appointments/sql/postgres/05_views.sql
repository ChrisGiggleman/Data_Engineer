DROP VIEW IF EXISTS v_appointments_enriched;

CREATE VIEW v_appointments_enriched AS
SELECT
  *,
  (appointment_at - booked_at) AS lead_time_days
FROM appointments;
