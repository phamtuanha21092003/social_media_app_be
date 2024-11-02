from marshmallow import fields
from .base import BaseSerializer


class SerializerAccountUser(BaseSerializer):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    is_active = fields.Boolean()
    avatar = fields.String()
    is_friend = fields.Method("get_is_friend")


    def get_is_friend(self, user):
        return user.friend_id is not None


    def _add_prefetch_data(self, records):
        pass
