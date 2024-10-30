"""update type status account_friend_ship

Revision ID: 2c6734d873af
Revises: da11899d8e6e
Create Date: 2024-10-29 13:36:41.801202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c6734d873af'
down_revision: Union[str, None] = 'da11899d8e6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # this upgrade should not downgrade
    # if downgrade fix this function to pass
    op.execute(sa.text("""ALTER TYPE account_friendship_status ADD VALUE 'DELETED'"""))



def downgrade() -> None:
    pass
