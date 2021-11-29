"""add content column to posts table

Revision ID: 6f687f340922
Revises: c284ec7f1e5e
Create Date: 2021-11-29 13:14:33.856038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6f687f340922"
down_revision = "c284ec7f1e5e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
