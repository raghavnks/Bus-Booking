"""One-time DB bootstrap: creates the app role and database on the Postgres
server, using the target credentials from backend/.env and an admin login
you enter interactively (never passed as a CLI arg or committed anywhere).

Run this yourself, directly in a terminal (not through an AI assistant),
since it prompts for your Postgres admin password:

    cd backend
    .venv\\Scripts\\activate
    python scripts\\bootstrap_db.py
"""

import getpass
import sys
from pathlib import Path

import psycopg2
from psycopg2 import sql

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import get_settings  # noqa: E402

settings = get_settings()


def main() -> None:
    admin_user = input("Postgres admin user [postgres]: ") or "postgres"
    admin_password = getpass.getpass("Postgres admin password: ")

    conn = psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname="postgres",
        user=admin_user,
        password=admin_password,
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (settings.POSTGRES_USER,))
            if cur.fetchone() is None:
                cur.execute(
                    sql.SQL("CREATE ROLE {} LOGIN PASSWORD %s").format(
                        sql.Identifier(settings.POSTGRES_USER)
                    ),
                    (settings.POSTGRES_PASSWORD,),
                )
                print(f"Created role '{settings.POSTGRES_USER}'.")
            else:
                print(f"Role '{settings.POSTGRES_USER}' already exists, skipping.")

            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.POSTGRES_DB,))
            if cur.fetchone() is None:
                cur.execute(
                    sql.SQL("CREATE DATABASE {} OWNER {}").format(
                        sql.Identifier(settings.POSTGRES_DB), sql.Identifier(settings.POSTGRES_USER)
                    )
                )
                print(f"Created database '{settings.POSTGRES_DB}' owned by '{settings.POSTGRES_USER}'.")
            else:
                print(f"Database '{settings.POSTGRES_DB}' already exists, skipping.")
    finally:
        conn.close()

    print("Done. You can now run: alembic upgrade head")


if __name__ == "__main__":
    main()
