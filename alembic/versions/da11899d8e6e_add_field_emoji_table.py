"""add field emoji table

Revision ID: da11899d8e6e
Revises: f783333c89ea
Create Date: 2024-10-16 13:37:39.208854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da11899d8e6e'
down_revision: Union[str, None] = 'f783333c89ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'emoji',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('url', sa.String(length=255), nullable=False),
    )

    op.add_column(
        'chat_conversation_message',
        sa.Column('emoji_id', sa.Integer(), sa.ForeignKey("emoji.id"), nullable=True, index=True)
    )


def downgrade() -> None:
    op.drop_column('chat_conversation_message', 'emoji_id')

    op.drop_table('emoji')