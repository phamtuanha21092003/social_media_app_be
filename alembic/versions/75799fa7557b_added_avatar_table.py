"""Added avatar table

Revision ID: 75799fa7557b
Revises: 968bd051882f
Create Date: 2024-06-23 14:19:02.739783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models import AvatarStatus


# revision identifiers, used by Alembic.
revision: str = '75799fa7557b'
down_revision: Union[str, None] = '968bd051882f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "avatar",
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True, index=True),
        sa.Column('account_user_id', sa.Integer(), sa.ForeignKey("account_user.id"), nullable=False, index=True),
        sa.Column('url', sa.String(length=255), nullable=False, index=True),    
        sa.Column('status', sa.String(length=25), nullable=False, index=True, default=AvatarStatus.ACTIVE.value),
        sa.Column('created', sa.DateTime(), default=sa.func.current_timestamp()),
        sa.Column('updated', sa.DateTime(), default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
    )




def downgrade() -> None:
    op.drop_table("avatar")
