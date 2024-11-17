from app.services.models.base import BaseModelService
from models.emoji import Emoji


class EmojiService(BaseModelService):
    def __init__(self):
        self.model = Emoji
