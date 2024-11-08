from .base import BaseModel, TimestampModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import typing


if typing.TYPE_CHECKING:
    from .account_user import AccountUser



class ConversationUser(BaseModel, TimestampModel):
    __tablename__ = "chat_conversation_user"

    account_user_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    account_user: Mapped["AccountUser"] = relationship(back_populates="conversation_users")

    conversation_id: Mapped[int] = mapped_column(ForeignKey("chat_conversation.id"), nullable=False, index=True)
