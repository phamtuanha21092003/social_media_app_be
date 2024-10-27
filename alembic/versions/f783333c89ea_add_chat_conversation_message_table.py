"""add chat_conversation_message table

Revision ID: f783333c89ea
Revises: 88e008260380
Create Date: 2024-10-16 11:31:26.725057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f783333c89ea'
down_revision: Union[str, None] = '88e008260380'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'chat_conversation_message',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp(), index=True),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.Column('creator_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('target_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('conversation_id', sa.Integer(), sa.ForeignKey("chat_conversation.id"), nullable=False, index=True),
        sa.Column('content', sa.String(length=255), nullable=False, index=True),
    )



def downgrade() -> None:
    op.drop_table('chat_conversation_message')
