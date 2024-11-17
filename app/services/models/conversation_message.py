from app.services.models.base import BaseModelService
from models.conversation_message import ConversationMessage


class ConversationMessageService(BaseModelService):
    def __init__(self):
        self.model = ConversationMessage


    def get_messages(self, conversation_id: int, limit: int, offset: int, avatars: dict):
        messages, total = self.find(conversation_id=conversation_id, is_get_total=True, order_bys=[ConversationMessage.created.desc()])

        messages = [
            {
                "id": message.id,
                "content": message.content if message.status != "DELETED" else "The message has been deleted",
                "emoji_id": message.emoji_id,
                "creator_id": message.creator_id,
                "status": message.status,
                'created': message.created,
                'avatar': avatars[message.creator_id]
            }
            for message in messages
        ]

        return messages, total
