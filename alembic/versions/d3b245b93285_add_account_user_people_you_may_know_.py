"""add account_user_people_you_may_know table

Revision ID: d3b245b93285
Revises: 69fb151639b8
Create Date: 2024-09-23 13:08:19.030255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3b245b93285'
down_revision: Union[str, None] = '69fb151639b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'account_user_people_you_may_know',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('creator_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('target_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp())
    )


def downgrade() -> None:
    op.drop_table('account_user_people_you_may_know')
