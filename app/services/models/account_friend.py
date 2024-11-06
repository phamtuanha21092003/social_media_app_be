from models.account_friend import AccountFriend
from app.services.models.base import BaseModelService
from sqlalchemy import Select, or_, and_



class AccountFriendService(BaseModelService):
    def __init__(self) -> None:
        self.model = AccountFriend


    def is_friend(self, creator_id: int, target_id: int):
        friend = self.session.scalars(
            Select(self.model).where(
                or_(
                    and_(
                        self.model.creator_id == creator_id,
                        self.model.target_id == target_id
                    ),
                    and_(
                        self.model.creator_id == target_id,
                        self.model.target_id == creator_id
                    )
                )
            )
        ).first()

        return friend is not None, friend.id if friend is not None else 0
