from marshmallow import fields
from .. import BaseSchema



class GetFriendsRequestSchema(BaseSchema):
    keyword = fields.Str()



class UpdateProfileRequestSchema(BaseSchema):
    name = fields.Str()
    phone = fields.Str()
    address = fields.Str()
    avatar = fields.Str()