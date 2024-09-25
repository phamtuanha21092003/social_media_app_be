from typing import List
from sqlalchemy import or_, select, text
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
            .filter(or_(AccountFriend.creator_id == id, AccountFriend.target_id == id), AccountUser.id != id)

        total = self.get_total(query)

        friends = self.session.scalars(query.limit(limit).offset(offset)).all() 

        return total, friends


    def get_friend_suggestions(self, id: int, limit: int, offset: int):
        # todo: add paging

        query_str = text("""
            SELECT au.*, av.url as avatar
            FROM account_user au
            LEFT JOIN avatar av
                ON av.account_user_id = au.id
            LEFT JOIN account_user_people_you_may_know aupymk 
                ON aupymk.creator_id  = au.id OR aupymk.target_id = au.id
            WHERE au.id != :id AND au.id NOT IN (
                SELECT 
                  CASE 
                    WHEN creator_id = :id THEN target_id 
                    ELSE creator_id 
                  END AS friend_id
                FROM account_friend af
                WHERE af.creator_id = :id OR af.target_id = :id	
            )
            ORDER BY 
            	CASE
                    WHEN aupymk.id IS NULL THEN 2
                    ELSE 1
                END
        """)

        return self.session.execute(query_str, {'id': id}).all()

