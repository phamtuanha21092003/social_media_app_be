from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from models.base import BaseModel


class AccountUserPeopleYouMayKnow(BaseModel):
    __tablename__ = 'account_user_people_you_may_know'

    creator_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)

    target_id: Mapped[int] = mapped_column(ForeignKey("account_user.id"), nullable=False, index=True)