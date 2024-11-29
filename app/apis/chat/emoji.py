from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.services.models.emoji import EmojiService
from app.utils import to_dict
from app.services.validators import validate_params
from app.services.validators.chat.emoji import GetEmojiSchema


class Emojis(Resource):
    def __init__(self):
        self.emoji_service = EmojiService()


    @jwt_required()
    @validate_params(GetEmojiSchema)
    def get(self):
        kwargs = {}

        is_detail_post = self.params.get("is_detail_post")
        if is_detail_post:
            kwargs["id"] = [21, 31, 32, 33, 34]

        emojis = self.emoji_service.find(**kwargs)

        emojis = {emoji.id: emoji.url for emoji in emojis}

        return {'data': to_dict(emojis), 'message': 'success'}

