"""add post_like table

Revision ID: e80657314201
Revises: 468c8a2b270e
Create Date: 2024-11-18 22:42:53.085245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e80657314201'
down_revision: Union[str, None] = '468c8a2b270e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post_like",
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('account_user_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey("post.id"), nullable=False, index=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
    )

    op.add_column("post", sa.Column("like_count", sa.Integer(), nullable=True, server_default='0'))


def downgrade() -> None:
    op.drop_table("post_like")
    op.drop_column("post", "like_count")
