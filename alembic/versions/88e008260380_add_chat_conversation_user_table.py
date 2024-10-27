"""add chat_conversation_user table

Revision ID: 88e008260380
Revises: 955b03645894
Create Date: 2024-10-16 09:37:13.371535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88e008260380'
down_revision: Union[str, None] = '955b03645894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'chat_conversation_user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp(), index=True),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('account_user_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('conversation_id', sa.Integer(), sa.ForeignKey("chat_conversation.id"), nullable=False, index=True),
    )



def downgrade() -> None:
    op.drop_table('chat_conversation_user')
