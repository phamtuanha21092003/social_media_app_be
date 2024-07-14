from app.services.validators import BaseSchema
from marshmallow import fields




class LoginRequestSchema(BaseSchema):
    email = fields.Email(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)