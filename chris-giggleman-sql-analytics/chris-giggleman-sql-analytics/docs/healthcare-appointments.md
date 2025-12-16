---
layout: page
title: Healthcare Appointments
---

**Repo folder:** `03_healthcare_appointments`

## What you'll find
- `data/raw/` sample CSVs
- `sql/sqlite/` scripts (create → clean → analyze)
- `sql/postgres/` scripts (create → \copy load → clean → analyze)
- Views + data quality tests

## Recommended screenshots for recruiters
- ERD + table list
- 2–3 KPI result tables from `04_analysis.sql`
- One “insight” query output (top segment, churn drivers, no-show drivers)

## Run order
**SQLite:** `01_create_tables.sql` → import CSV → `03_cleaning.sql` → `04_analysis.sql`  
**Postgres:** `01_create_tables.sql` → `02_load_data.sql` → `03_cleaning.sql` → `04_analysis.sql`
