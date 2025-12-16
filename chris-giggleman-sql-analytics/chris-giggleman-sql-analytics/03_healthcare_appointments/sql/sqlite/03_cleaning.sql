-- Cleaning (SQLite)

UPDATE appointments
SET clinic = TRIM(clinic),
    provider = NULLIF(TRIM(provider), ''),
    status = TRIM(status),
    insurance_type = TRIM(insurance_type);

-- Standardize status values
UPDATE appointments SET status = 'NoShow'    WHERE LOWER(status) IN ('noshow','no show','no_show');
UPDATE appointments SET status = 'Canceled'  WHERE LOWER(status) IN ('cancelled','canceled');
UPDATE appointments SET status = 'Completed' WHERE LOWER(status) IN ('complete','completed');

-- Remove provider blanks -> set to 'Unknown' for grouping (explicitly documented)
UPDATE appointments SET provider = 'Unknown' WHERE provider IS NULL;
