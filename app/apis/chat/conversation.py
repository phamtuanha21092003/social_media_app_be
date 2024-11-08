from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.conversation import ConversationService
from app.services.models.account_user import AccountUserService
from app.services.models.conversation_user import ConversationUserService
from app.common.errors import UNotFound
from db import session_scope


class Conversations(Resource):

    @jwt_required()
    def get(self):
        pass


    @jwt_required()
    def post(self):
        user_id = current_user.id


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



