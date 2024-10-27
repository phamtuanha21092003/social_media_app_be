from models.account_user_people_you_may_know import AccountUserPeopleYouMayKnow
from app.services.models.base import BaseModelService
from sqlalchemy import select, or_, and_

class AccountUserPeopleYouMayKnowService(BaseModelService):
    def __init__(self) -> None:
        self.model = AccountUserPeopleYouMayKnow


    def remove_suggesstions(self, creator_id: int, taget_id: int):
        query = select(self.model).where(
            or_(
                and_(
                    self.model.creator_id == creator_id,
                    self.model.target_id == taget_id,
                ),
                and_(
                    self.model.creator_id == taget_id,
                    self.model.target_id == creator_id,
                )
            ),
        )

        suggestions = self.session.scalars(query).all()

        for suggestion in suggestions:
            self.delete(suggestion)
