"""create index column title post table

Revision ID: 3c9d362bf964
Revises: 2c6734d873af
Create Date: 2024-10-31 11:06:51.673885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c9d362bf964'
down_revision: Union[str, None] = '2c6734d873af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_post_title', 'post', ['title'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_post_title', 'post')
