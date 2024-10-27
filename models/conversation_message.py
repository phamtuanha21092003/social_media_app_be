from .base import BaseModel, TimestampModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import typing


if typing.TYPE_CHECKING:
    from .account_user import AccountUser



class ConversationMessage(BaseModel, TimestampModel):
    __tablename__ = "chat_conversation_message"

    creator_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    creator: Mapped[AccountUser] = relationship(foreign_keys=[creator_id])

    target_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)
    target: Mapped[AccountUser] = relationship(foreign_keys=[target_id])

    conversation_id: Mapped[int] = mapped_column(ForeignKey("chat_conversation.id"), nullable=False, index=True)

    content: Mapped[str] = mapped_column(nullable=False)
