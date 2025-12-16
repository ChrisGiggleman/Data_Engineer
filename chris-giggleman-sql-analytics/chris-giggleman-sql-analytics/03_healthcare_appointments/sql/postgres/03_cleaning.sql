UPDATE appointments
SET clinic = BTRIM(clinic),
    provider = NULLIF(BTRIM(provider), ''),
    status = BTRIM(status),
    insurance_type = NULLIF(BTRIM(insurance_type), '');

UPDATE appointments SET status = 'NoShow'    WHERE LOWER(status) IN ('noshow','no show','no_show');
UPDATE appointments SET status = 'Canceled'  WHERE LOWER(status) IN ('cancelled','canceled');
UPDATE appointments SET status = 'Completed' WHERE LOWER(status) IN ('complete','completed');

UPDATE appointments SET provider = 'Unknown' WHERE provider IS NULL;
