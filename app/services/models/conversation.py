from app.services.models.base import BaseModelService
from models.conversation import Conversation



class ConversationService(BaseModelService):
    def __init__(self):
        self.model = Conversation