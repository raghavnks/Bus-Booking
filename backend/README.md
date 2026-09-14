# BusBooking — Business Services (Backend)

FastAPI service holding the core booking business logic (routes, buses, bookings, ...).
First vertical slice: the `routes` domain (origin/destination/distance), backed by PostgreSQL.

## Structure

```
app/
  api/v1/endpoints/   route handlers (HTTP layer only)
  core/                settings/config
  db/                  SQLAlchemy engine/session, declarative base
  models/              SQLAlchemy ORM models
  schemas/             Pydantic request/response models
  services/            business logic, called by endpoints
  tests/               pytest suite
alembic/               DB migrations
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements-dev.txt

copy .env.example .env        # then fill in POSTGRES_PASSWORD etc.
```

The Postgres server is expected at `192.168.29.225:5432` (already provisioned). Update
`.env` with real credentials and a database that exists on that server — this service
does not create the database itself, only its own tables via Alembic.

## Run migrations

```bash
alembic upgrade head
```

## Run the service

```bash
uvicorn app.main:app --reload
```

- Liveness: `GET /api/v1/health/live`
- Readiness (checks DB): `GET /api/v1/health/ready`
- Routes API: `GET/POST /api/v1/routes`, `GET /api/v1/routes/{id}`
- Interactive docs: `http://localhost:8000/docs`

## Quality gates

```bash
ruff check .        # lint
pytest               # unit/integration tests
bandit -r app -ll    # SAST
pip-audit -r requirements.txt   # dependency vulnerability scan
```

These also run in CI (`.github/workflows/ci.yml`) on every push/PR. DAST (e.g. OWASP ZAP
against a running instance) will be added once there's a deployed environment to point it at.
