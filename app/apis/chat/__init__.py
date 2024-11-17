from flask import Blueprint
from flask_restful import Api
from .conversation import ConversationCreateOrGet, Conversations
from .message import Message, MessageDelete

chat_blueprint = Blueprint("chat_blueprint", __name__, url_prefix="/chat")
chat_api = Api(chat_blueprint)


chat_resources = {
    '/conversations/<int:user_id>/create_or_get': ConversationCreateOrGet,
    '/conversations': Conversations,
    '/messages/<int:conversation_id>': Message,
    '/messages/<int:message_id>/delete': MessageDelete,
}


for url_path, view in chat_resources.items():
    chat_api.add_resource(
        view, '{}/'.format(url_path)
    )
