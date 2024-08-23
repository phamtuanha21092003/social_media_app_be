from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.account_user import AccountUserService
from app.services.models.avatar_service import AvatarService
from app.services.serializers.account_user import SerializerAccountUser
from app.services.validators import  validate_body
from app.services.validators.profile import UpdateProfileRequestSchema
from db import session_scope


class Me(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()
        self.avatar_service = AvatarService()


    @jwt_required()
    def get(self):
        return { 'message': '', 'data': SerializerAccountUser().dump_data(current_user) }


    @jwt_required()
    @validate_body(UpdateProfileRequestSchema)
    def post(self):
        with session_scope():
            avatar_url = self.body.get('avatar')

            self.body.pop('avatar', None)

            self.account_user_service.update(current_user, **self.body)

            if avatar_url:
                avatar = self.avatar_service.first(account_user_id=current_user.id)

                if avatar:
                    self.avatar_service.update(avatar, url=avatar_url)

                else:
                    self.avatar_service.create(account_user_id=current_user.id, url=avatar_url)

        return { 'message': 'Update successfully' }