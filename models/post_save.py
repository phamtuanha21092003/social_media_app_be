from .base import BaseModel, TimestampModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class PostSave(BaseModel, TimestampModel):
    __tablename__ = "post_save"

    account_user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False, index=True)