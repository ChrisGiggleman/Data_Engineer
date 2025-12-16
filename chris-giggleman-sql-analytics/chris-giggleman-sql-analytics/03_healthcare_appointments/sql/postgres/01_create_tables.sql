DROP TABLE IF EXISTS appointments;

CREATE TABLE appointments (
  appointment_id  INT PRIMARY KEY,
  patient_id      INT NOT NULL,
  clinic          TEXT NOT NULL,
  provider        TEXT,
  booked_at       DATE NOT NULL,
  appointment_at  DATE NOT NULL,
  status          TEXT NOT NULL,
  insurance_type  TEXT
);

CREATE INDEX idx_appt_patient ON appointments(patient_id);
CREATE INDEX idx_appt_clinic ON appointments(clinic);
CREATE INDEX idx_appt_provider ON appointments(provider);
