from sqlalchemy import select
from models import AccountUser
from .base import BaseModelService
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.common.errors import UPermissionDenied


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
