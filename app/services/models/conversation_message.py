from app.services.models.base import BaseModelService
from models.conversation_message import ConversationMessage


class ConversationMessageService(BaseModelService):
    def __init__(self):
        self.model = ConversationMessage