from flask_restful import Resource
from app.services.validators.auth.sign_up import SignUpRequestSchema
from app.services import validate_body
from app.services.models import AccountUserService
from db import session_scope

class SignUp(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @validate_body(SignUpRequestSchema)
    def post(self):
        with session_scope():
            self.account_user_service.sign_up(**self.body)

        return {'message': 'User created successfully'}