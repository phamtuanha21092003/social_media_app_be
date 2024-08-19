"""add account_friend_table

Revision ID: 6341c277c6a7
Revises: 2c01545d70ec
Create Date: 2024-08-13 11:21:52.056691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6341c277c6a7'
down_revision: Union[str, None] = '2c01545d70ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'account_friend',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('creator_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('target_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    op.drop_table("account_friend")