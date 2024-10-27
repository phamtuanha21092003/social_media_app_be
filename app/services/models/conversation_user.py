from app.services.models.base import BaseModelService
from models.conversation_user import ConversationUser


class ConversationUserService(BaseModelService):
    def __init__(self):
        self.model = ConversationUser