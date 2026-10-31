"""add users and trip ownership

Revision ID: 0003_users_trip_owner
Revises: 0002_categories_expenses
Create Date: 2026-10-31
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0003_users_trip_owner"
down_revision: str | None = "0002_categories_expenses"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Old local rows predate authentication, so this migration keeps their owner empty.
    # New application code always writes a user_id for newly created trips.
    with op.batch_alter_table("trips") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_trips_user_id_users", "users", ["user_id"], ["id"])
        batch_op.create_index("ix_trips_user_id", ["user_id"])


def downgrade() -> None:
    with op.batch_alter_table("trips") as batch_op:
        batch_op.drop_index("ix_trips_user_id")
        batch_op.drop_constraint("fk_trips_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
