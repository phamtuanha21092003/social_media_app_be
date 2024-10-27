from marshmallow import fields
from app.services.models.account_user import AccountUserService
from app.services.models.comment import CommentService
from .base import ModelSerializer, serializer_date_time



class SerializerPost(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.comment_service = CommentService()

        self.account_user_service = AccountUserService()


    title = fields.String()
    url = fields.String()
    comments = fields.Method('get_comments')
    created = fields.DateTime('%Y-%m-%d %H:%M:%S+00:00')
    account_user_id = fields.Integer()
    comment_count = fields.Integer()
    like_count = fields.Integer()
    avatar = fields.Method("get_avatar")
    name = fields.Method("get_name")


    def get_avatar(self, post):
        return self.prefetch_data.get('users', {}).get(post.account_user_id).avatar


    def get_name(self, post):
        return self.prefetch_data.get('users', {}).get(post.account_user_id).name


    def get_comments(self, post):
        comments = self.prefetch_data.get('comments', {}).get(post.id, [])

        users = self.prefetch_data.get('users', {})

        result = {}

        for _comment in comments:
            if not result.get(_comment.reply_id):
                result[_comment.reply_id] = []

            result[_comment.reply_id].append({
                'id': _comment.id,
                'title': _comment.title,
                'created': serializer_date_time(_comment.created),
                'avatar': users.get(_comment.account_user_id).avatar,
                'name': users.get(_comment.account_user_id).name,
                'user_account_id': _comment.account_user_id,
                "reply_count": _comment.reply_count,
            })

        return result


    def _add_prefetch_data(self, records):
        user_ids = set()

        if 'comments' in self.exclude or (self.only and 'comments' not in self.only):
            for _post in records:
                user_ids.add(_post.account_user_id)

            users = self.account_user_service.find(id=list(user_ids))

            self._add_prefetch_data_model(users, 'id', 'users')

            return

        post_ids = { record.id for record in records }

        comments = self.comment_service.find(post_id=list(post_ids), order_bys=[self.comment_service.model.created.desc()])


        for _post in records:
            user_ids.add(_post.account_user_id)

        for _comment in comments:
            user_ids.add(_comment.account_user_id)

        users = self.account_user_service.find(id=list(user_ids))

        self._add_prefetch_data_model(comments, 'post_id', 'comments', many=True)

        self._add_prefetch_data_model(users, 'id', 'users')