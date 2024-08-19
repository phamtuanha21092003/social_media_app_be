from models.account_friend import AccountFriend
from app.services.models.base import BaseModelService


class AccountFriendService(BaseModelService):
    def __init__(self) -> None:
        self.model = AccountFriend