-- One-time DB bootstrap. Run as a Postgres superuser (e.g. `postgres`), connected
-- to the default `postgres` database:
--   psql -h 192.168.29.225 -U postgres -d postgres -f bootstrap_db.sql
--
-- Replace the placeholders below with the same values you put in backend/.env
-- before running (POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB).

CREATE ROLE busbooking LOGIN PASSWORD 'change-me';
CREATE DATABASE busbooking OWNER busbooking;
