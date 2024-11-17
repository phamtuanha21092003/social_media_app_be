from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.services.models.emoji import EmojiService
from app.utils import to_dict


class Emojis(Resource):
    def __init__(self):
        self.emoji_service = EmojiService()


    @jwt_required()
    def get(self):
        emojis = self.emoji_service.find()

        emojis = {emoji.id: emoji.url for emoji in emojis}

        return {'data': to_dict(emojis), 'message': 'success'}

