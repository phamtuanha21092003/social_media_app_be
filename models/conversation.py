from .base import BaseModel, TimestampModel



class Conversation(BaseModel, TimestampModel):
    __tablename__ = "chat_conversation"


