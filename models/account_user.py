from sqlalchemy import desc
from .base import BaseModel, TimestampModel
from typing import List, TYPE_CHECKING
from .avatar import Avatar
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .avatar import Avatar


class AccountUser(BaseModel, TimestampModel):
    __tablename__ = "account_user"

    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    last_login: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    avatars: Mapped[List["Avatar"]] = relationship(order_by=lambda: [Avatar.status, desc(Avatar.created)],)


    @property
    def avatar(self):
        pass
