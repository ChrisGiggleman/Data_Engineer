-- Healthcare analysis (SQLite)

-- Lead time in days (appointment - booked)
SELECT
  appointment_id,
  patient_id,
  clinic,
  provider,
  status,
  ROUND(julianday(appointment_at) - julianday(booked_at), 0) AS lead_time_days
FROM appointments
ORDER BY lead_time_days ASC;

-- No-show rate by clinic/provider
WITH base AS (
  SELECT
    clinic,
    provider,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'NoShow' THEN 1 ELSE 0 END) AS noshows
  FROM appointments
  GROUP BY 1,2
)
SELECT
  clinic,
  provider,
  total,
  noshows,
  ROUND(100.0 * noshows / total, 2) AS noshow_pct
FROM base
ORDER BY noshow_pct DESC, total DESC;

-- Lead time buckets and no-show rate
WITH enriched AS (
  SELECT
    *,
    CASE
      WHEN (julianday(appointment_at) - julianday(booked_at)) <= 1 THEN '0-1 days'
      WHEN (julianday(appointment_at) - julianday(booked_at)) <= 7 THEN '2-7 days'
      WHEN (julianday(appointment_at) - julianday(booked_at)) <= 14 THEN '8-14 days'
      ELSE '15+ days'
    END AS lead_bucket
  FROM appointments
)
SELECT
  lead_bucket,
  COUNT(*) AS total,
  SUM(CASE WHEN status='NoShow' THEN 1 ELSE 0 END) AS noshows,
  ROUND(100.0 * SUM(CASE WHEN status='NoShow' THEN 1 ELSE 0 END) / COUNT(*), 2) AS noshow_pct
FROM enriched
GROUP BY 1
ORDER BY 1;

-- Repeat no-show patients
SELECT
  patient_id,
  COUNT(*) AS total_appts,
  SUM(CASE WHEN status='NoShow' THEN 1 ELSE 0 END) AS noshows
FROM appointments
GROUP BY 1
HAVING noshows >= 2
ORDER BY noshows DESC, total_appts DESC;
