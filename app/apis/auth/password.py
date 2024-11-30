from flask_bcrypt import check_password_hash, generate_password_hash
from flask_restful import Resource

from app import UPermissionDenied
from app.services import validate_body
from app.services.validators.auth.password import ChangePasswordRequestSchema
from app.services.models.account_user import AccountUserService
from db import session_scope
from flask_jwt_extended import jwt_required, current_user


class ChangePassword(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_body(ChangePasswordRequestSchema)
    def post(self):
        old_password = self.body["old_password"]
        new_password = self.body["new_password"]

        if not check_password_hash(current_user.password, old_password):
            raise UPermissionDenied('Old password is invalid')

        with session_scope():
            current_user.password = generate_password_hash(new_password).decode('utf-8')

            return {"message": "success"}
