from app.services.models.base import BaseModelService
from models.post_save import PostSave


class PostSaveService(BaseModelService):
    def __init__(self):
        self.model = PostSave
