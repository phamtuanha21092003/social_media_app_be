"""add status to chat_conversation_message

Revision ID: 468c8a2b270e
Revises: 3c9d362bf964
Create Date: 2024-11-11 14:58:15.873481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '468c8a2b270e'
down_revision: Union[str, None] = '3c9d362bf964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conversation_message_status = sa.Enum('ACTIVE', 'DELETED', name='conversation_message_status')
    conversation_message_status.create(op.get_bind())

    op.add_column('chat_conversation_message', sa.Column('status', conversation_message_status, nullable=False, default='ACTIVE', index=True))




def downgrade() -> None:
    op.drop_column('chat_conversation_message', 'status')

    sa.Enum('ACTIVE', 'DELETED', 'CANCELED', name='conversation_message_status').drop(op.get_bind())

