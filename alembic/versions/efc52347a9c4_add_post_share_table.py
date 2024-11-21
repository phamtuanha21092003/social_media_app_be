"""add post_share table

Revision ID: efc52347a9c4
Revises: 8d57547308aa
Create Date: 2024-11-20 19:24:38.429705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efc52347a9c4'
down_revision: Union[str, None] = '8d57547308aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post_share",
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('account_user_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey("post.id"), nullable=False, index=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
    )



def downgrade() -> None:
    op.drop_table("post_share")
