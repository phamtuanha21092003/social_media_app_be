from app.services.models.base import BaseModelService
from models.post import Post


class PostService(BaseModelService):
    def __init__(self):
        self.model = Post