from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.conversation import ConversationService
from app.services.models.account_user import AccountUserService
from app.services.models.conversation_user import ConversationUserService
from app.services.models.conversation_message import ConversationMessageService
from app.common.errors import UNotFound, UPermissionDenied
from db import session_scope
from app.services.validators import validate_params, get_limit_from_page, validate_body, PagingSchema
from app.services.validators.chat.message import CreateMessageSchema
from app.utils import to_dict


class Message(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.account_user_service = AccountUserService()
        self.conversation_service = ConversationService()
        self.conversation_user_service = ConversationUserService()
        self.conversation_message_service = ConversationMessageService()


    # TODO: fix this api
    @jwt_required()
    @validate_params(PagingSchema)
    def get(self, conversation_id: int):
        user_id = current_user.id

        conversation = self.conversation_service.find_by_id(conversation_id)
        if not conversation:
            raise UNotFound(f'Conversation with id {conversation_id} not found')

        conversation_users = self.conversation_user_service.find(conversation_id=conversation_id)
        if len(conversation_users) == 0:
            raise UNotFound(f'Conversation with id {conversation_id} not found')

        if user_id not in [_conversation_user.account_user_id for _conversation_user in conversation_users]:
            raise UNotFound(f'Conversation with id {conversation_id} not found')

        limit, offset = get_limit_from_page(self.params)

        avatars = self.account_user_service.get_avatars([_conversation_user.account_user_id for _conversation_user in conversation_users])

        messages, total = self.conversation_message_service.get_messages(conversation_id, limit, offset, avatars)

        for _conversation_user in conversation_users:
            if _conversation_user.account_user_id != user_id:
                user_id = _conversation_user.account_user_id
                break

        user = self.account_user_service.find_by_id(user_id)

        return {
            "messages": to_dict(messages),
            "total": total,
            "is_active": user.is_active,
            "last_login": to_dict(user.last_login),
            'name': user.name,
            'avatar': user.avatar,
            'user_id': user.id,
            "message": "success",
        }



    @jwt_required()
    @validate_body(CreateMessageSchema)
    def post(self, conversation_id: int):
        user_id = current_user.id

        conversation = self.conversation_service.find_by_id(conversation_id)
        if not conversation:
            raise UNotFound(f'Conversation with id {conversation_id} not found')

        conversation_users = self.conversation_user_service.find(conversation_id=conversation_id)
        if len(conversation_users) == 0:
            raise UNotFound(f'Conversation with id {conversation_id} not found')

        if user_id not in [_conversation_user.account_user_id for _conversation_user in conversation_users]:
            raise UNotFound(f'Conversation with id {conversation_id} not found')

        content = self.body.get('content')

        for _conversation_user in conversation_users:
            if user_id != _conversation_user.account_user_id:
                target_id = _conversation_user.account_user_id

        with session_scope():
            self.conversation_message_service.create(content=content, target_id=target_id, creator_id=user_id, conversation_id=conversation_id)

            return {"message": "success"}



class MessageDelete(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.account_user_service = AccountUserService()
        self.conversation_message_service = ConversationMessageService()


    @jwt_required()
    def delete(self, message_id:int):
        user_id = current_user.id

        message = self.conversation_message_service.find_by_id(message_id)
        if not message:
            raise UNotFound(f'Message with id {message_id} not found')

        if message.creator_id != user_id:
            raise UPermissionDenied(f'Message with id {message_id} not found')

        with session_scope():
            self.conversation_message_service.update(message, status="DELETED")

            return {"message": "success"}
