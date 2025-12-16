# SQL Data Analyst Portfolio (SQLite + PostgreSQL)

This repo contains **4 end-to-end SQL projects** designed to showcase data analyst skills:
- Data modeling (schemas + constraints)
- Loading data from CSV
- Data cleaning (nulls/blanks, standardization, deduping, integrity fixes)
- Analytical SQL (KPIs, segmentation, cohorts, churn, window functions)
- Reproducible setup for **SQLite** and **PostgreSQL**

## Projects
1. **Retail Sales Analytics** (`01_retail_sales_analytics`)
2. **HR Attrition & Pay Equity** (`02_hr_attrition`)
3. **Healthcare Appointments & No-Show Drivers** (`03_healthcare_appointments`)
4. **SaaS Subscriptions: MRR & Churn** (`04_saas_subscriptions`)

## Quick start
### Option A — SQLite (fastest)
1. Install DB Browser for SQLite (GUI) and/or SQLite CLI.
2. For a project, open its `*.db` (or create one) and run scripts in order:
   - `sql/sqlite/01_create_tables.sql`
   - import CSVs from `data/raw/*.csv`
   - `sql/sqlite/03_cleaning.sql`
   - `sql/sqlite/04_analysis.sql`
   - optional: `sql/sqlite/05_views.sql`, `sql/sqlite/06_tests.sql`

### Option B — PostgreSQL (Docker)
1. Install Docker Desktop
2. From repo root:
   ```bash
   cd 00_setup/postgres
   docker compose up -d
   ```
3. Connect with your SQL client (DBeaver/pgAdmin) using:
   - Host: `localhost`
   - Port: `5432`
   - DB: `portfolio`
   - User: `portfolio`
   - Password: `portfolio`
4. For a project, run scripts in order:
   - `sql/postgres/01_create_tables.sql`
   - `sql/postgres/02_load_data.sql` (uses `\copy`)
   - `sql/postgres/03_cleaning.sql`
   - `sql/postgres/04_analysis.sql`
   - optional: `sql/postgres/05_views.sql`, `sql/postgres/06_tests.sql`

## Data generation (optional)
If you want bigger datasets, use:
- `utils/data_generator/` (Python + Faker)

## GitHub Pages (optional)
A ready-to-host site is included in `/docs`.

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Source: Deploy from a branch → Branch: `main` → Folder: `/docs`
4. Open your published site and link it on your resume/LinkedIn.

## Mermaid diagrams
Each project README includes a Mermaid ERD. GitHub renders Mermaid automatically in Markdown.

