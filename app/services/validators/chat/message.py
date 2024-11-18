from .. import BaseSchema
from marshmallow import fields


class CreateMessageSchema(BaseSchema):
    content = fields.Str(required=True)



class MessageEmojiSchema(BaseSchema):
    emoji_id = fields.Int(required=True)
