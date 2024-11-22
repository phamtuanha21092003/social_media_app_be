from marshmallow import fields
from .base import BaseSerializer


class SerializerAccountUser(BaseSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from app.services.models import AccountUserService
        self.account_user_service = AccountUserService()


    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    is_active = fields.Boolean()
    avatar = fields.String()
    last_login = fields.DateTime('%Y-%m-%d %H:%M:%S+00:00')
    is_friend = fields.Method("get_is_friend")
    count_friend = fields.Method("get_count_friend")


    def get_is_friend(self, user):
        return user.friend_id is not None


    def get_count_friend(self, user):
        return self.account_user_service.count_friends(user.id)


    def _add_prefetch_data(self, records):
        pass
