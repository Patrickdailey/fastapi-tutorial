"""add FK to posts table

Revision ID: d233e050ac03
Revises: b6e618ba6f32
Create Date: 2021-11-29 13:30:20.221095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d233e050ac03"
down_revision = "b6e618ba6f32"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
