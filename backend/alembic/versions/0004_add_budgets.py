"""Add user-owned budgets.

Revision ID: 0004_add_budgets
Revises: 0003_add_users_and_trip_ownership
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_add_budgets"
down_revision = "0003_add_users_and_trip_ownership"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("trip_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("trip_id IS NOT NULL OR category_id IS NOT NULL", name="ck_budgets_has_target"),
        sa.CheckConstraint("amount > 0", name="ck_budgets_positive_amount"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["trip_id"], ["trips.id"]),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
    )
    op.create_index("ix_budgets_user_id", "budgets", ["user_id"])
    op.create_index("ix_budgets_trip_id", "budgets", ["trip_id"])
    op.create_index("ix_budgets_category_id", "budgets", ["category_id"])


def downgrade() -> None:
    op.drop_index("ix_budgets_category_id", table_name="budgets")
    op.drop_index("ix_budgets_trip_id", table_name="budgets")
    op.drop_index("ix_budgets_user_id", table_name="budgets")
    op.drop_table("budgets")
