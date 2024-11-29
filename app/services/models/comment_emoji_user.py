from app.services.models.base import BaseModelService
from models.comment_emoji_user import CommentEmojiUser


class CommentEmojiUserService(BaseModelService):
    def __init__(self):
        self.model = CommentEmojiUser
