from typing import List
from sqlalchemy import or_, select, text
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from models.account_friend import AccountFriend
from models import AccountUser
from app.common.errors import UPermissionDenied
from .base import BaseModelService
from sqlalchemy import Select


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
        user_id = user.id

        return access_token, refresh_token, user_id


    def get_friends(self, id: int, limit: int, offset: int, keyword) -> tuple[int, List[AccountUser]]:
        query = select(AccountUser, )\
            .join(AccountFriend, or_(AccountFriend.target_id == AccountUser.id, AccountFriend.creator_id == AccountUser.id))\
            .filter(or_(AccountFriend.creator_id == id, AccountFriend.target_id == id), AccountUser.id != id)

        if keyword:
            query = query.filter(AccountUser.name.ilike(f'%{keyword}%'))

        total = self.get_total(query)

        friends = self.session.scalars(query.limit(limit).offset(offset)).all() 

        return total, friends


    # todo: fix this api use 1 raw query
    # this function get all user not is friend of this user
    # order by if have in account_user_people_you_may_know
    def get_friend_suggestions(self, id: int, limit: int, offset: int):
        query = text(
            """
                SELECT au.id, au.name, a.url as avatar
                FROM account_user au
                LEFT JOIN avatar a ON a.account_user_id = au.id
                WHERE au.id IN (
                    SELECT
                        CASE 
                            WHEN creator_id = :id THEN target_id
                            ELSE creator_id
                        END AS id
                    FROM account_user_people_you_may_know
                    WHERE creator_id = :id OR target_id = :id
                    LIMIT 5
                    OFFSET 0
                )
            """
        )

        return self.session.execute(query, {'id': id}).all()


    # co qua ton ram k khi k co limit offset
    # orm thi phuc tap ???
    # raw query thi met ???
    def get_friend_ids(self, user_id: int):
        pass



    def get_users_by_keyword(self, keyword: str, limit: int, offset: int, user_id: int) -> tuple[List[AccountUser], int]:
        query_total = Select(self.model).where(self.model.name.ilike(f'%{keyword}%'))

        total = self.get_total(query_total)

        query_str = """
            SELECT au."name", au.email, au.id, au.is_active, f.id as friend_id
            FROM account_user au 
            LEFT JOIN (
                SELECT CASE 
                    WHEN af.creator_id = :user_id THEN af.target_id
                    ELSE af.creator_id
                END AS id
                FROM account_friend af 
                WHERE creator_id = :user_id OR target_id = :user_id
            ) f
            ON f.id = au.id
            WHERE au."name" ILIKE :keyword
            ORDER BY f.id
            LIMIT :limit
            OFFSET :offset
        """

        return self.session.execute(text(query_str), {'user_id': user_id, 'keyword': f'%{keyword}%', 'limit': limit, 'offset': offset}).all(), total
