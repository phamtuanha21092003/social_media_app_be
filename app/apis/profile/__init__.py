from flask import Blueprint
from flask_restful import Api
from .friends import Friends, Friend, FriendShips, FriendSuggestion
from .me import Me


profile_blueprint = Blueprint("profile_blueprint", __name__, url_prefix="/profile")
profile_api = Api(profile_blueprint)


profile_routers = {
    '/friends': Friends,
    '/friend/<int:target_id>': Friend,
    '/me': Me,
    '/friendships': FriendShips,
    '/friend_suggestions': FriendSuggestion,
    # todo: api cancel friendship
}


for url_path, view in profile_routers.items():
    profile_api.add_resource(
        view, '{}/'.format(url_path)
    )
