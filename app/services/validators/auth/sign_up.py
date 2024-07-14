from app.services.validators import BaseSchema
from marshmallow import fields



class SignUpRequestSchema(BaseSchema):
    email = fields.Email(required=True, allow_none=False)
    name = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)