from app.services.validators import BaseSchema
from marshmallow import fields


class CommentsRequestSchema(BaseSchema):
    title = fields.Str(required=True, allow_none=False)
    reply_id = fields.Integer()