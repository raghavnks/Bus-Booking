"""Insert sample records into the `employees` table of the BusBooking DB.

Run:

    cd backend
    .venv\\Scripts\\activate
    python scripts\\insert_sample_employee.py
"""

import sys
from pathlib import Path

import psycopg2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import get_settings  # noqa: E402

settings = get_settings()

SAMPLE_EMPLOYEES = [
    ("Jane", "Doe", "jane.doe@example.com", "Driver"),
    ("John", "Smith", "john.smith@example.com", "Conductor"),
    ("Priya", "Sharma", "priya.sharma@example.com", "Dispatcher"),
    ("Carlos", "Ruiz", "carlos.ruiz@example.com", "Driver"),
    ("Aiko", "Tanaka", "aiko.tanaka@example.com", "Mechanic"),
]


def main() -> None:
    conn = psycopg2.connect(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    role TEXT NOT NULL
                )
                """
            )
            cur.executemany(
                """
                INSERT INTO employees (first_name, last_name, email, role)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
                """,
                SAMPLE_EMPLOYEES,
            )
        conn.commit()
        print(f"Inserted {len(SAMPLE_EMPLOYEES)} sample employees (existing ones skipped).")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
