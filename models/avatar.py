from .base import BaseModel, TimestampModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import enum
import typing


if typing.TYPE_CHECKING:
    from models import AccountUser


class AvatarStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"



class Avatar(BaseModel, TimestampModel):
    __tablename__ = "avatar"

    url: Mapped[str] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(default=AvatarStatus.ACTIVE.value, nullable=False)

    account_user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    account_user: Mapped["AccountUser"] = relationship(back_populates="avatars")
