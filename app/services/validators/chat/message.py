from .. import BaseSchema
from marshmallow import fields


class CreateMessageSchema(BaseSchema):
    content = fields.Str(required=True)
