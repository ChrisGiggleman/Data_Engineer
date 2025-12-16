# PostgreSQL Setup (Docker)

## Prereqs
- Docker Desktop
- SQL client: DBeaver or pgAdmin

## Start database
```bash
cd 00_setup/postgres
docker compose up -d
```

## Connection
- Host: localhost
- Port: 5432
- Database: portfolio
- User: portfolio
- Password: portfolio

## Loading CSV
Each project includes `sql/postgres/02_load_data.sql` using `\copy`, which works in **psql**.
If you're using a GUI, you can import CSV via the client UI instead.

To use psql inside the container:
```bash
docker exec -it portfolio_postgres psql -U portfolio -d portfolio
```
