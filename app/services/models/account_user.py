from typing import List
from sqlalchemy import or_, select
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from models.account_friend import AccountFriend
from models import AccountUser
from app.common.errors import UPermissionDenied
from .base import BaseModelService


class AccountUserService(BaseModelService):
    def __init__(self) -> None:
        self.model = AccountUser


    def sign_up(self, **kwargs):
        kwargs['password'] = generate_password_hash(kwargs['password']).decode('utf-8')
        self.create(**kwargs)


    def login(self, email: str, password: str):
        user = self.session.scalars(
                select(self.model).
                filter_by(email=email)
            ).first()

        if not user:
            raise UPermissionDenied('Email, password are invalid')

        if not check_password_hash(user.password, password):
            raise UPermissionDenied('Email, password are invalid')

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        return access_token, refresh_token


    def get_friends(self, id: int, limit: int, offset: int) -> tuple[int, List[AccountUser]]:
        query = select(AccountUser, )\
            .join(AccountFriend, or_(AccountFriend.target_id == AccountUser.id, AccountFriend.creator_id == AccountUser.id))\
            .filter(or_(AccountFriend.creator_id == id, AccountFriend.target_id == id))

        total = self.get_total(query)

        friends = self.session.scalars(query.limit(limit).offset(offset)).all() 

        return total, friends