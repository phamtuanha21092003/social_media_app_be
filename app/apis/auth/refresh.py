from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user
from flask_restful import Resource
from app.services.models.account_user import AccountUserService
from db import session_scope
import datetime


class Refresh(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required(refresh=True)
    def post(self):
        with session_scope():
            access_token = create_access_token(identity=current_user, fresh=False)
            refresh_token = create_refresh_token(identity=current_user)

            self.account_user_service.update(current_user, last_login=datetime.datetime.now(datetime.timezone.utc))

            return {'access_token': access_token, 'refresh_token': refresh_token}
