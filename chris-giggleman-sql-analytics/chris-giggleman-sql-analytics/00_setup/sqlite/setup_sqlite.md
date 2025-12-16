# SQLite Setup (Windows/macOS/Linux)

## Tools
- **DB Browser for SQLite** (GUI) — easiest for importing CSV and running scripts
- Optional: **SQLite CLI**
- Optional: VS Code extensions: "SQLite" (alexcvzz)

## Steps (DB Browser)
1. Open DB Browser for SQLite
2. Create a new database file (e.g. `retail.db`)
3. Open `sql/sqlite/01_create_tables.sql` from the project and run it
4. Import CSVs from `data/raw/` into their matching tables (File → Import → Table from CSV)
5. Run:
   - `sql/sqlite/03_cleaning.sql`
   - `sql/sqlite/04_analysis.sql`

## Notes
- SQLite stores dates as TEXT (ISO-8601 like `YYYY-MM-DD`), which works well for analytics.
