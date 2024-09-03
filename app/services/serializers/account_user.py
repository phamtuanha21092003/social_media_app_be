from marshmallow import fields
from .base import BaseSerializer


class SerializerAccountUser(BaseSerializer):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    is_active = fields.Boolean()
    avatar = fields.String()


    def _add_prefetch_data(self, records):
        pass
