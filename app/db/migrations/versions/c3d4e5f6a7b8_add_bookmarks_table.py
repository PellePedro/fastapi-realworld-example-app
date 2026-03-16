"""add bookmarks table

Revision ID: c3d4e5f6a7b8
Revises: fdf8821871d7
Create Date: 2026-03-16 00:00:00.000000

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

revision = "c3d4e5f6a7b8"
down_revision = "fdf8821871d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bookmarks",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "article_id",
            sa.Integer,
            sa.ForeignKey("articles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("note", sa.Text, nullable=False, server_default=""),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )
    op.create_primary_key("pk_bookmarks", "bookmarks", ["user_id", "article_id"])


def downgrade() -> None:
    op.drop_table("bookmarks")
