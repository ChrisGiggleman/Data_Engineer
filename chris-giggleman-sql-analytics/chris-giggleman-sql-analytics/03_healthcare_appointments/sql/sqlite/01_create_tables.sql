DROP TABLE IF EXISTS appointments;

CREATE TABLE appointments (
  appointment_id  INTEGER PRIMARY KEY,
  patient_id      INTEGER NOT NULL,
  clinic          TEXT NOT NULL,
  provider        TEXT,
  booked_at       TEXT NOT NULL,
  appointment_at  TEXT NOT NULL,
  status          TEXT NOT NULL,  -- Completed/NoShow/Canceled
  insurance_type  TEXT
);

CREATE INDEX idx_appt_patient ON appointments(patient_id);
CREATE INDEX idx_appt_clinic ON appointments(clinic);
CREATE INDEX idx_appt_provider ON appointments(provider);
