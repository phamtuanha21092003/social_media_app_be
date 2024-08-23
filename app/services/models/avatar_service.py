from app.services.models.base import BaseModelService
from models.avatar import Avatar


class AvatarService(BaseModelService):
    def __init__(self) -> None:
        self.model = Avatar