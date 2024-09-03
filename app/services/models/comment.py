from app.services.models.base import BaseModelService
from models.comment import Comment


class CommentService(BaseModelService):
    def __init__(self):
        self.model = Comment