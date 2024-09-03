from marshmallow import fields
from sqlalchemy import text
from app.services.models.account_user import AccountUserService
from app.services.models.comment import CommentService
from .base import BaseSerializer, serializer_date_time



class SerializerPost(BaseSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.comment_service = CommentService()

        self.account_user_service = AccountUserService()


    id = fields.Integer()
    title = fields.String()
    url = fields.String()
    comments = fields.Method('get_comments')
    created = fields.DateTime('%Y-%m-%d %H:%M:%S')
    account_user_id = fields.Integer()
    comment_count = fields.Integer()


    def get_comments(self, post):
        comments = self.prefetch_data.get('comments', {}).get(post.id, [])

        comment_replies = { _comment.id: self.prefetch_data.get('comment_replies', {}).get(_comment.id, []) for _comment in comments }

        return [
            {
                'id': _comment.id,
                'title': _comment.title,
                'created': serializer_date_time(_comment.created),
                'avatar': self.prefetch_data.get('users', {}).get(_comment.account_user_id).avatar,
                'user_account_id': _comment.account_user_id,
                "reply_count": _comment.reply_count,
                "replies": [
                    { "id": _reply.id, "title": _reply.title, "created": serializer_date_time(_reply.created), "reply_count": _reply.reply_count, 'avatar': self.prefetch_data.get('users', {}).get(_reply.account_user_id).avatar, 'user_account_id': _reply.account_user_id }
                    for _reply in comment_replies[_comment.id]
                ]
            }
            for _comment in comments
        ]


    def _add_prefetch_data(self, records):
        if 'comments' in self.exclude or ( self.only and 'comments' not in self.only ):
            return

        if self.many:
            post_ids = { record.id for record in records }
        else:
            post_ids = { records.id }

        query_comments = """
            SELECT post_id, id, title, created, reply_count, account_user_id, index
            FROM (
                SELECT post_id, id, title, created, reply_count, account_user_id, ROW_NUMBER() OVER(PARTITION BY post_id ORDER BY created DESC) as index
                FROM comment
                WHERE post_id IN :post_ids
            )
            WHERE index <= 3
        """

        comments = self.session.execute(text(query_comments), { "post_ids": tuple(post_ids) }).all()

        comment_ids = { comment.id for comment in comments }

        comment_replies = self.comment_service.find(reply_id=list(comment_ids))

        user_ids = set()

        for _comment in comments:
            user_ids.add(_comment.account_user_id)

        for _comment in comment_replies:
            user_ids.add(_comment.account_user_id)

        users = self.account_user_service.find(id=list(user_ids))

        self._add_prefetch_data_model(comments, 'post_id', 'comments', many=True)

        self._add_prefetch_data_model(comment_replies, 'reply_id', 'comment_replies', many=True)

        self._add_prefetch_data_model(users, 'id', 'users')