"""add comment table

Revision ID: eac112efc892
Revises: 9723fdf2c02a
Create Date: 2024-08-29 11:03:04.471821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eac112efc892'
down_revision: Union[str, None] = '9723fdf2c02a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comment",
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('account_user_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey("post.id",  ondelete='CASCADE'), nullable=False),
        sa.Column('reply_id', sa.Integer, sa.ForeignKey('comment.id',  ondelete='CASCADE'), nullable=True, default=None),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    op.drop_table("comment")
