-- Healthcare analysis (PostgreSQL)

-- Lead time in days
SELECT
  appointment_id,
  patient_id,
  clinic,
  provider,
  status,
  (appointment_at - booked_at) AS lead_time_days
FROM appointments
ORDER BY lead_time_days;

-- No-show rate by clinic/provider
WITH base AS (
  SELECT
    clinic,
    provider,
    COUNT(*) AS total,
    SUM(CASE WHEN status='NoShow' THEN 1 ELSE 0 END) AS noshows
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

-- Lead time buckets
WITH enriched AS (
  SELECT
    *,
    CASE
      WHEN (appointment_at - booked_at) <= 1 THEN '0-1 days'
      WHEN (appointment_at - booked_at) <= 7 THEN '2-7 days'
      WHEN (appointment_at - booked_at) <= 14 THEN '8-14 days'
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
