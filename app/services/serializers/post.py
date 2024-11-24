from marshmallow import fields
from app.services.models.account_user import AccountUserService
from app.services.models.comment import CommentService
from app.services.models.post_like import PostLikeService
from app.services.models.post_save import PostSaveService
from .base import ModelSerializer, serializer_date_time
from flask_jwt_extended import current_user



class SerializerPost(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.comment_service = CommentService()

        self.account_user_service = AccountUserService()

        self.post_like_service = PostLikeService()

        self.post_save_service = PostSaveService()


    title = fields.String()
    url = fields.String()
    comments = fields.Method('get_comments')
    created = fields.DateTime('%Y-%m-%d %H:%M:%S+00:00')
    account_user_id = fields.Integer()
    comment_count = fields.Integer()
    like_count = fields.Integer()
    avatar = fields.Method("get_avatar")
    name = fields.Method("get_name")
    is_liked = fields.Method("get_is_liked")
    is_saved = fields.Method("get_is_saved")
    status = fields.String()


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
                "post_id": _comment.post_id,
            })

        return result


    def get_is_liked(self, post):
        post_id = post.id

        post_like = self.prefetch_data.get("post_likes", {}).get(post_id)

        return post_like is not None


    def get_is_saved(self, post):
        post_id = post.id

        post_save = self.prefetch_data.get("post_saves", {}).get(post_id)

        return post_save is not None


    def _add_prefetch_data(self, records):
        user_ids = set()

        post_ids = {record.id for record in records}

        user_id = current_user.id

        post_likes = self.post_like_service.find(post_id=list(post_ids), account_user_id=user_id)
        self._add_prefetch_data_model(post_likes, 'post_id', 'post_likes')

        post_saves = self.post_save_service.find(post_id=list(post_ids), account_user_id=user_id)
        self._add_prefetch_data_model(post_saves, 'post_id', 'post_saves')

        if 'comments' in self.exclude or (self.only and 'comments' not in self.only):
            for _post in records:
                user_ids.add(_post.account_user_id)

            users = self.account_user_service.find(id=list(user_ids))

            self._add_prefetch_data_model(users, 'id', 'users')

            return

        comments = self.comment_service.find(post_id=list(post_ids), order_bys=[self.comment_service.model.created.desc()])

        for _post in records:
            user_ids.add(_post.account_user_id)

        for _comment in comments:
            user_ids.add(_comment.account_user_id)

        users = self.account_user_service.find(id=list(user_ids))

        self._add_prefetch_data_model(comments, 'post_id', 'comments', many=True)

        self._add_prefetch_data_model(users, 'id', 'users')