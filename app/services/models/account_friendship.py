from models.account_friendship import AccountFriendship
from app.services.models.base import BaseModelService
from sqlalchemy import select, or_, and_
from app.common.errors import UBadRequest

class AccountFriendshipService(BaseModelService):
    def __init__(self) -> None:
        self.model = AccountFriendship


    def add_friend(self, user_id: int, target_id: int):
        friendship = self.first(creator_id=user_id, target_id=target_id)

        if friendship:
            if friendship.status in ['CANCELED', 'DELETED']:
                self.update(friendship, status='PENDING')
                return

            raise UBadRequest("Friendship does exist")

        self.create(creator_id=user_id, target_id=target_id)


    def get_friendship(self, creator_id: int, target_id: int, **kwargs) -> AccountFriendship | None:
        query = select(self.model).where(
            or_(
                and_(
                    self.model.creator_id == creator_id,
                    self.model.target_id == target_id,
                ),
                and_(
                    self.model.creator_id == target_id,
                    self.model.target_id == creator_id,
                )
            )
        )

        query = self.where(query, **kwargs)

        friendship = self.session.scalars(query).first()

        return friendship


    def get_friendships(self, creator_id: int, target_id: int, **kwargs) -> list:
        query = select(self.model).where(
            or_(
                and_(
                    self.model.creator_id == creator_id,
                    self.model.target_id == target_id,
                ),
                and_(
                    self.model.creator_id == target_id,
                    self.model.target_id == creator_id,
                )
            )
        )

        query = self.where(query, **kwargs)

        return self.session.scalars(query).all()
