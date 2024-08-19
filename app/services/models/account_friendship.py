from models.account_friendship import AccountFriendship
from app.services.models.base import BaseModelService


class AccountFriendshipService(BaseModelService):
    def __init__(self) -> None:
        self.model = AccountFriendship