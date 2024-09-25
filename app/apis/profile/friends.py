from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.account_user import AccountUserService
from app.services.models.account_friendship import AccountFriendshipService
from app.services.models.account_friend import AccountFriendService
from app.services import validate_params, validate_body
from app.services.serializers import SerializerAccountUser
from app.services.validators import get_limit_from_page, PagingSchema
from app.services.validators.profile import GetFriendsRequestSchema, ConfirmFriendShipPostRequestSchema
from app.common.errors import UNotFound
from db import session_scope
from app.utils.dict import to_dict


class Friends(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_params(GetFriendsRequestSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        total,  friends = self.account_user_service.get_friends(user_id, limit, offset)

        return {"total": total, "data": SerializerAccountUser(many=True).dump_data(friends)}



class Friend(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()
        self.account_friendship_service = AccountFriendshipService()


    @jwt_required()
    def post(self, target_id: int):
        user_id = current_user.id

        target = self.account_user_service.find_by_id(target_id)

        if not target:
            raise UNotFound('User not found')

        with session_scope():
            self.account_friendship_service.add_friend(user_id, target_id)

            return {"message": "Add friend successfully"}


    @jwt_required()
    def delete(self):
        # todo: api delete friend
        pass


class FriendShips(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()
        self.account_friendship_service = AccountFriendshipService()
        self.account_friend_service = AccountFriendService()


    @jwt_required()
    def get(self):
        # todo: add paging in this api
        user_id = current_user.id

        friendships, total = self.account_friendship_service.find(target_id=user_id, status="PENDING", order_bys=[self.account_friendship_service.model.created.desc()], is_get_total=True, limit=10, offset=0)

        return {'data': to_dict(friendships), 'total': total}


    @jwt_required()
    @validate_body(ConfirmFriendShipPostRequestSchema)
    def post(self):
        target_id = current_user.id

        creator_id = self.body.get('creator_id')

        friendship = self.account_friendship_service.first(creator_id=creator_id, target_id=target_id)

        if not friendship:
            raise UNotFound('Friendship not found')

        with session_scope():
            self.account_friendship_service.update(friendship, status="ACCEPTED")
            self.account_friend_service.create(creator_id=creator_id, target_id=target_id)
            return {"message": "Friendship has been accepted"}



class FriendSuggestion(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_params(PagingSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        friend_suggestions = self.account_user_service.get_friend_suggestions(user_id, limit, offset)

        return {"data": SerializerAccountUser(many=True).dump_data(friend_suggestions), 'total': len(friend_suggestions)}