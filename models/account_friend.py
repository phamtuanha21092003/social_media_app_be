from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.account_user import AccountUser
from models.base import BaseModel, TimestampModel


class AccountFriend(BaseModel, TimestampModel):
    __tablename__ = 'account_friend'

    creator_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    creator: Mapped[AccountUser] = relationship(foreign_keys=[creator_id])

    target_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    target: Mapped[AccountUser] = relationship(foreign_keys=[target_id])
