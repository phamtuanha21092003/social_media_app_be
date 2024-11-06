from flask import Blueprint
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Api, Resource
from .friends import Friends, Friend, FriendShips, FriendSuggestion, FriendShipCancel, FriendDelete
from .me import Me
from ...services.models import AccountUserService
from ...services.models.avatar_service import AvatarService
from app.common.errors import UNotFound
from app.services.models.account_friend import AccountFriendService
from app.services.models.account_friendship import AccountFriendshipService


profile_blueprint = Blueprint("profile_blueprint", __name__, url_prefix="/profile")
profile_api = Api(profile_blueprint)


class Profile(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()
        self.avatar_service = AvatarService()
        self.account_friend_service = AccountFriendService()
        self.account_friendship_service = AccountFriendshipService()


    @jwt_required()
    def get(self, user_id: int):
        id = current_user.id

        user = self.account_user_service.find_by_id(user_id)
        if not user:
            raise UNotFound("user not found")

        data = {}

        if id != user_id:
            friendship = self.account_friendship_service.get_friendship(status="PENDING", creator_id=user_id, target_id=id)
            if friendship:
                data["is_sent_request"] = True
                data["from_id"] = friendship.creator_id

            else:
                is_friend, friend_id = self.account_friend_service.is_friend(id, user_id)
                data["is_friend"] = is_friend
                data["friend_id"] = friend_id

        return {
            'message': 'success',
            'data': {
                **data,
                'id': user_id,
                'avatar': user.avatar,
                'name': user.name,
                'is_active': user.is_active,
                'email': user.email,
            }
        }




profile_routers = {
    '/friends': Friends,
    '/friend/<int:target_id>': Friend,
    '/me': Me,
    '/friendships': FriendShips,
    '/friendship/<int:target_id>/cancel': FriendShipCancel,
    '/friend_suggestions': FriendSuggestion,
    '/<int:user_id>': Profile,
    '/friend/<int:friend_id>/delete': FriendDelete,
}


for url_path, view in profile_routers.items():
    profile_api.add_resource(
        view, '{}/'.format(url_path)
    )
