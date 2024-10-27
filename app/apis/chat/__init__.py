from flask import Blueprint
from flask_restful import Api

chat_blueprint = Blueprint("chat_blueprint", __name__, url_prefix="/chat")
chat_api = Api(chat_blueprint)


chat_resources = {

}


for url_path, view in chat_resources.items():
    chat_api.add_resource(
        view, '{}/'.format(url_path)
    )
