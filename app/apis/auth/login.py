from flask_restful import Resource
from app.services import validate_body
from app.services.validators.auth.login import LoginRequestSchema
from app.services.models.account_user import AccountUserService



class Login(Resource):
    def __init__(self) -> None:
        self.acount_user_service = AccountUserService()


    @validate_body(LoginRequestSchema)
    def post(self):
        access_token, refresh_token = self.acount_user_service.login(**self.body)

        return { 'access_token': access_token, 'refresh_token': refresh_token }