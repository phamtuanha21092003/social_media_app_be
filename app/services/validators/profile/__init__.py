from marshmallow import fields
from .. import BaseSchema



class GetFriendsRequestSchema(BaseSchema):
    keyword = fields.Str()