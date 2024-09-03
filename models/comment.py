from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import typing
from .base import BaseModel, TimestampModel


if typing.TYPE_CHECKING:
    from .account_user import AccountUser
    from .post import Post



class Comment(BaseModel, TimestampModel):
    __tablename__ = "comment"

    title: Mapped[str] = mapped_column(nullable=False)
    reply_count: Mapped[int] = mapped_column(default=0)

    account_user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    account_user: Mapped["AccountUser"] = relationship(back_populates="comments")

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=True, index=True)
    post: Mapped["Post"] = relationship(back_populates="comments")

    reply_id: Mapped[int] = mapped_column(ForeignKey("comment.id"))
    replies:  Mapped[typing.List["Comment"]] = relationship("Comment", back_populates="reply", lazy="dynamic")
    reply: Mapped["Comment"] = relationship("Comment", back_populates="replies", remote_side="[Comment.id]")