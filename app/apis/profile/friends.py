from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.account_user import AccountUserService
from app.services import validate_params
from app.services.serializers import SerializerAccountUser
from app.services.validators import get_limit_from_page
from app.services.validators.profile import GetFriendsRequestSchema
from app.common.errors import UNotFound



class Friends(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_params(GetFriendsRequestSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        total,  friends = self.account_user_service.get_friends(user_id, limit, offset)

        return { "total": total, "data": SerializerAccountUser().dump_data(friends, many=True) }



class Friend(Resource):
    def __init__(self) -> None:
        self.account_user_service = AccountUserService()


    @jwt_required()
    def post(self, target_id: int):
        user_id = current_user.id

        target = self.account_user_service.find_by_id(target_id)

        if not target:
            raise UNotFound('User not found')

        self.account_user_service.add_friend(user_id, self.params['target_id'])

        return { "message": "Add friend successfully" }


    @jwt_required()
    def delete(self):
        user_id = current_user.id

        self.account_user_service.remove_friend(user_id, self.params['target_id'])

        return { "message": "Remove friend successfully" }