from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.conversation import ConversationService
from app.services.models.account_user import AccountUserService
from app.services.models.conversation_user import ConversationUserService
from app.common.errors import UNotFound
from app.utils import to_dict
from db import session_scope
from app.services.validators import PagingSchema, validate_params, get_limit_from_page


class Conversations(Resource):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.account_user_service = AccountUserService()
        self.conversation_service = ConversationService()
        self.conversation_user_service = ConversationUserService()


    @jwt_required()
    @validate_params(PagingSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        conversations, total = self.conversation_service.get_conversation_ids_and_total(user_id, limit, offset)

        conversations_dict = {}
        user_ids = []
        for _conversation in conversations:
            user_ids.append(_conversation["user_id"])
            conversations_dict[_conversation["user_id"]] = _conversation

        users = self.account_user_service.find(id=user_ids)

        users_dict = {user.id: user for user in users}

        for _conversation in list(conversations):
            _conversation["avatar"] = users_dict[_conversation["user_id"]].avatar
            _conversation["name"] = users_dict[_conversation["user_id"]].name

        return {"data": to_dict(conversations), "total": total, "message": "success"}



class ConversationCreateOrGet(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.account_user_service = AccountUserService()
        self.conversation_service = ConversationService()
        self.conversation_user_service = ConversationUserService()


    @jwt_required()
    def post(self, user_id: int):
        creator_id = current_user.id

        if creator_id == user_id:
            raise UNotFound("User not found")

        user = self.account_user_service.find_by_id(user_id)
        if not user:
            raise UNotFound("User not found")

        conversation = self.conversation_service.get_conversation_by_user_ids(creator_id, user_id)
        if not conversation:
            with session_scope(is_close=False):
                conversation = self.conversation_service.create()

                self.conversation_user_service.create(account_user_id=creator_id, conversation_id=conversation.id)
                self.conversation_user_service.create(account_user_id=user_id, conversation_id=conversation.id)

        return {"message": "success", "id": conversation.id}


