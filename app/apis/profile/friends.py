from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.account_user import AccountUserService
from app.services.models.account_friendship import AccountFriendshipService
from app.services.models.account_friend import AccountFriendService
from app.services import validate_params, validate_body
from app.services.serializers import SerializerAccountUser
from app.services.validators import get_limit_from_page, PagingSchema
from app.services.validators.profile import GetFriendsRequestSchema, ConfirmFriendShipPostRequestSchema, \
    FriendshipGetRequestSchema, DeleteFriendShipRequestSchema
from app.services.models.account_user_people_you_may_know import AccountUserPeopleYouMayKnowService
from app.common.errors import UNotFound
from db import session_scope, db


class Friends(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_params(GetFriendsRequestSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        keyword = self.params.get("keyword")

        total,  friends = self.account_user_service.get_friends(user_id, limit, offset, keyword)

        return {"total": total, "data": SerializerAccountUser(many=True, exclude=["is_friend"]).dump_data(friends)}



class Friend(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()
        self.account_friendship_service = AccountFriendshipService()
        self.account_user_people_you_may_know_service = AccountUserPeopleYouMayKnowService()


    @jwt_required()
    def post(self, target_id: int):
        user_id = current_user.id

        target = self.account_user_service.find_by_id(target_id)

        if not target:
            raise UNotFound('User not found')

        with session_scope():
            self.account_friendship_service.add_friend(user_id, target_id)
            self.account_user_people_you_may_know_service.remove_suggesstions(user_id, target_id)

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
        self.session = db.session


    @jwt_required()
    @validate_params(FriendshipGetRequestSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        status = self.params.get("status")
        keyword = self.params.get("keyword")

        kwargs = {
            'joiners': [(self.account_friendship_service.model, self.account_user_service.model.id == self.account_friendship_service.model.creator_id), ],
            'is_get_query': True,
        }

        query = self.account_user_service.find(**kwargs)

        query = query.filter(self.account_friendship_service.model.target_id == user_id)

        if keyword:
            query = query.filter(self.account_user_service.model.name.ilike(f'%{keyword}%'))

        if status:
            query = query.filter(self.account_friendship_service.model.status.in_(status))

        total = self.account_user_service.get_total(query)

        query = query.order_by(self.account_friendship_service.model.created.desc()).limit(limit).offset(offset)

        users = self.session.scalars(query).all()

        return {'data': SerializerAccountUser(many=True, exclude=["is_friend"]).dump_data(users), 'total': total}


    @jwt_required()
    @validate_body(ConfirmFriendShipPostRequestSchema)
    def post(self):
        target_id = current_user.id

        creator_id = self.body.get('creator_id')

        friendship = self.account_friendship_service.first(creator_id=creator_id, target_id=target_id, status="PENDING")

        if not friendship:
            raise UNotFound('Friendship is existing')

        with session_scope():
            self.account_friendship_service.update(friendship, status="ACCEPTED")
            self.account_friend_service.create(creator_id=creator_id, target_id=target_id)
            return {"message": "Friendship has been accepted"}


    @jwt_required()
    @validate_body(DeleteFriendShipRequestSchema)
    def delete(self):
        target_id = current_user.id

        creator_id = self.body.get('creator_id')

        friendship = self.account_friendship_service.first(creator_id=creator_id, target_id=target_id, status="PENDING")

        if not friendship:
            raise UNotFound('Friendship is not found')

        with session_scope():
            self.account_friendship_service.update(friendship, status="DELETED")
            return {"message": "success"}





class FriendSuggestion(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_params(PagingSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        friend_suggestions = self.account_user_service.get_friend_suggestions(user_id, limit, offset)

        return {"data": SerializerAccountUser(many=True, exclude=["is_friend"]).dump_data(friend_suggestions), 'total': len(friend_suggestions)}