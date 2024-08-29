import typing
from .base import BaseModel, TimestampModel
from .comment import Comment
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


if typing.TYPE_CHECKING:
    from .account_user import AccountUser


class Post(BaseModel, TimestampModel):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=True)

    account_user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    account_user: Mapped["AccountUser"] = relationship(back_populates="posts")

    comments: Mapped[typing.List["Comment"]] = relationship(back_populates="post", lazy="dynamic")