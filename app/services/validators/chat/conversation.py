from .. import BaseSchema
from marshmallow import fields


class CreateConversationPostRequestSchema(BaseSchema):
    target_id = fields.Integer(required=True, allow_none=False)
