from app.services.models.base import BaseModelService
from models.post_like import PostLike


class PostLikeService(BaseModelService):
    def __init__(self):
        self.model = PostLike
