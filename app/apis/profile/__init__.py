from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Api, Resource
from .friends import Friends, Friend, FriendShips, FriendSuggestion
from .me import Me
from ...services.models import AccountUserService
from ...services.models.avatar_service import AvatarService
from app.common.errors import UNotFound
from ...services.serializers import SerializerAccountUser

profile_blueprint = Blueprint("profile_blueprint", __name__, url_prefix="/profile")
profile_api = Api(profile_blueprint)


class Profile(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()
        self.avatar_service = AvatarService()


    @jwt_required()
    def get(self, user_id: int):
        user = self.account_user_service.find_by_id(user_id)
        if not user:
            raise UNotFound("user not found")

        return {'message': 'successfully', 'data': SerializerAccountUser(exclude=["is_friend"]).dump_data(user)}




profile_routers = {
    '/friends': Friends,
    '/friend/<int:target_id>': Friend,
    '/me': Me,
    '/friendships': FriendShips,
    '/friend_suggestions': FriendSuggestion,
    '/<int:user_id>': Profile,
    # todo: api cancel friendship
}


for url_path, view in profile_routers.items():
    profile_api.add_resource(
        view, '{}/'.format(url_path)
    )
