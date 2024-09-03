from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import desc
import typing

from models import comment
from .base import BaseModel, TimestampModel
from .avatar import Avatar
from .post import Post



class AccountUser(BaseModel, TimestampModel):
    __tablename__ = "account_user"

    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    last_login: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    avatars: Mapped[typing.List["Avatar"]] = relationship(
        "Avatar",
        primaryjoin="and_(AccountUser.id==Avatar.account_user_id, "
            "Avatar.status=='ACTIVE')",
        order_by=lambda: [desc(Avatar.created)],
        lazy="dynamic"
    )

    posts: Mapped[typing.List["Post"]] = relationship(
        back_populates="account_user",
        order_by=lambda: [desc(Post.created)],
        lazy="dynamic",
    )

    comments: Mapped[typing.List["comment.Comment"]] = relationship(back_populates="account_user", lazy="dynamic")

    @property
    def avatar(self):
        avatar = self.avatars.first()
        return avatar.url if avatar else "" 
