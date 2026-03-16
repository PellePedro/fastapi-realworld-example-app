"""add categories table

Revision ID: b2c3d4e5f6a7
Revises: fdf8821871d7
Create Date: 2026-03-16 00:00:00.000000

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

revision = "b2c3d4e5f6a7"
down_revision = "fdf8821871d7"
branch_labels = None
depends_on = None


def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.current_timestamp(),
        ),
    )


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, unique=True, nullable=False),
        sa.Column("slug", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_category_modtime
            BEFORE UPDATE
            ON categories
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def downgrade() -> None:
    op.drop_table("categories")
