"""add account friendship table

Revision ID: 2c01545d70ec
Revises: 75799fa7557b
Create Date: 2024-08-13 10:57:43.787802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c01545d70ec'
down_revision: Union[str, None] = '75799fa7557b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    account_friendship_status = sa.Enum('PENDING', 'ACCEPTED', 'CANCELED', name='account_friendship_status')

    account_friendship_status.create(op.get_bind())

    op.create_table(
        'account_friendship',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('status', account_friendship_status, nullable=False, default='PENDING', index=True),
        sa.Column('creator_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('target_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
    )



def downgrade() -> None:
    op.drop_table("account_friendship")

    sa.Enum('PENDING', 'ACCEPTED', 'CANCELED', name='account_friendship_status').drop(op.get_bind())
