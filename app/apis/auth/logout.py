from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.account_user import AccountUserService
from db import session_scope


class Logout(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()



    @jwt_required()
    def post(self):
        with session_scope():
            self.account_user_service.update(current_user, is_active=False)

            return {'message': 'success'}
