from models.account_friendship import AccountFriendship
from app.services.models.base import BaseModelService
from sqlalchemy import select, or_, and_
from app.common.errors import UBadRequest

class AccountFriendshipService(BaseModelService):
    def __init__(self) -> None:
        self.model = AccountFriendship


    def add_friend(self, user_id: int, target_id: int):
        friendship = self.session.scalars(select(self.model).where(
            or_(
                and_(
                    self.model.creator_id == user_id,
                    self.model.target_id == target_id,
                ),
                and_(
                    self.model.creator_id == target_id,
                    self.model.target_id == user_id,
                )
            )
        )).first()

        if friendship:
            if friendship.status == 'CANCEL':
                self.update(friendship, status='PENDING')
                return

            raise UBadRequest("Friendship does exist")

        self.create(creator_id=user_id, target_id=target_id)