from .. import BaseSchema
from marshmallow import fields


class GetEmojiSchema(BaseSchema):
    is_detail_post = fields.Boolean(allow_none=True)
