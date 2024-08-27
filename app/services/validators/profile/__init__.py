from marshmallow import RAISE, fields
from .. import BaseSchema



class GetFriendsRequestSchema(BaseSchema):
    keyword = fields.Str()



class UpdateProfileRequestSchema(BaseSchema):
    class Meta:
        unknown = RAISE

    name = fields.Str()
    phone = fields.Str()
    address = fields.Str()
    avatar = fields.Str()