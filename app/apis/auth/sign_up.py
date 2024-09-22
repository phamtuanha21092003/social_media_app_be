from flask_restful import Resource
from app.services.validators.auth.sign_up import SignUpRequestSchema
from app.services import validate_body
from app.services.models import AccountUserService
from db import session_scope
from app import UBadRequest

class SignUp(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @validate_body(SignUpRequestSchema)
    def post(self):
        email = self.body['email']
        user = self.account_user_service.first(email=email)
        if user:
            raise UBadRequest('Email already registered')

        with session_scope():
            self.account_user_service.sign_up(**self.body)

        return {'message': 'User created successfully'}