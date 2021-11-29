"""create posts table

Revision ID: c284ec7f1e5e
Revises: 
Create Date: 2021-11-29 13:02:37.557931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c284ec7f1e5e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop("posts")
    pass
