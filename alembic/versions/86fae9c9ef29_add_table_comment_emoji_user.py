"""add table comment_emoji_user

Revision ID: 86fae9c9ef29
Revises: 22dcd30a4b09
Create Date: 2024-11-28 01:03:50.373212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86fae9c9ef29'
down_revision: Union[str, None] = '22dcd30a4b09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'comment_emoji_user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp(), index=True),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('account_user_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('comment_id', sa.Integer(), sa.ForeignKey("comment.id", ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('emoji_id', sa.Integer(), sa.ForeignKey("emoji.id", ondelete='CASCADE'), nullable=False, index=True),
    )



def downgrade() -> None:
    op.drop_table('comment_emoji_user')
