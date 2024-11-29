from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import BaseModel, TimestampModel


class CommentEmojiUser(BaseModel, TimestampModel):
    __tablename__ = "comment_emoji_user"

    account_user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id", ondelete="CASCADE"), nullable=False)

    emoji_id: Mapped[int] = mapped_column(ForeignKey("emoji.id", ondelete="CASCADE"), nullable=False)

    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id", ondelete="CASCADE"), nullable=False)
