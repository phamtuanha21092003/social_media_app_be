"""add field comment_count, sub_comment_count

Revision ID: 69fb151639b8
Revises: eac112efc892
Create Date: 2024-08-31 18:04:06.514895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69fb151639b8'
down_revision: Union[str, None] = 'eac112efc892'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('comment_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('comment', sa.Column('reply_count', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    op.drop_column('post', 'comment_count')
    op.drop_column('comment', 'reply_count')
