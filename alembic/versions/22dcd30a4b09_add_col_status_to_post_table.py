"""add col status to post table

Revision ID: 22dcd30a4b09
Revises: efc52347a9c4
Create Date: 2024-11-21 14:55:19.947885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22dcd30a4b09'
down_revision: Union[str, None] = 'efc52347a9c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    post_status = sa.Enum('ACTIVE', 'DELETED', 'PRIVATE', name='post_status')
    post_status.create(op.get_bind())

    op.add_column('post', sa.Column('status', post_status, nullable=False, default='ACTIVE', index=True))


def downgrade() -> None:
    op.drop_column('chat_conversation_message', 'status')

    sa.Enum('ACTIVE', 'DELETED', 'PRIVATE', name='post_status').drop(op.get_bind())


