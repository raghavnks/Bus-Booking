"""create routes table

Revision ID: 0001
Revises:
Create Date: 2026-09-14

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "routes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("origin", sa.String(length=100), nullable=False),
        sa.Column("destination", sa.String(length=100), nullable=False),
        sa.Column("distance_km", sa.Numeric(7, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_routes_origin", "routes", ["origin"])
    op.create_index("ix_routes_destination", "routes", ["destination"])


def downgrade() -> None:
    op.drop_index("ix_routes_destination", table_name="routes")
    op.drop_index("ix_routes_origin", table_name="routes")
    op.drop_table("routes")
