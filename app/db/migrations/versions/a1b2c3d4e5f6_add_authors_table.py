"""add authors table

Revision ID: a1b2c3d4e5f6
Revises: fdf8821871d7
Create Date: 2026-03-16 00:00:00.000000

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

revision = "a1b2c3d4e5f6"
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
        "authors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        ),
        sa.Column("specialty", sa.Text, nullable=False, server_default=""),
        sa.Column("location", sa.Text, nullable=False, server_default=""),
        sa.Column("website", sa.Text, nullable=False, server_default=""),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_author_modtime
            BEFORE UPDATE
            ON authors
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def downgrade() -> None:
    op.drop_table("authors")
