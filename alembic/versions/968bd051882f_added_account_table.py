"""Added account table

Revision ID: 968bd051882f
Revises: 
Create Date: 2024-06-23 13:40:33.196668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '968bd051882f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'account_user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('name', sa.String(length=255), nullable=False, index=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('last_login', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
    )




def downgrade() -> None:
    op.drop_table("account_user")

