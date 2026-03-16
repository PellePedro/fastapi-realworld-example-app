"""add notifications table

Revision ID: d4e5f6a7b8c9
Revises: fdf8821871d7
Create Date: 2026-03-16 00:00:00.000000

"""
from typing import Tuple

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

revision = "d4e5f6a7b8c9"
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
        "notifications",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column(
            "is_read",
            sa.Boolean,
            nullable=False,
            server_default=sa.text("false"),
        ),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_notification_modtime
            BEFORE UPDATE
            ON notifications
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def downgrade() -> None:
    op.drop_table("notifications")
