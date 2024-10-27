from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.comment import CommentService
from app.services.models.post import PostService
from app.services.models import AccountUserService
from app.services.serializers.post import SerializerPost
from app.services.validators import get_limit_from_page, validate_body, validate_params
from app.services.validators.feed import CreatePostRequestSchema, GetPostRequestSchema
from app.services.validators.feed.post import CommentsRequestSchema
from db import session_scope
from app import UNotFound


class Posts(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_params(GetPostRequestSchema)
    def get(self):
        limit, offset = get_limit_from_page(self.params)

        user_id = self.params.get("user_id")

        kwargs = {
            'limit': limit,
            'offset': offset,
            'is_get_total': True,
            'order_bys': [self.post_service.model.created.desc()],
        }

        if user_id:
            user = self.account_user_service.find_by_id(user_id)
            if not user:
                raise UNotFound("User not found")

            kwargs.update({'account_user_id': user_id})

        posts, total = self.post_service.find(**kwargs)

        return {"total": total, "data": SerializerPost(many=True, exclude=["comments"]).dump_data(posts)}


    @jwt_required()
    @validate_body(CreatePostRequestSchema)
    def post(self):
        with session_scope():
            post = self.post_service.create(account_user_id=current_user.id, **self.body)

            return {'message': 'Created successfully', 'data': SerializerPost(exclude=["comments"]).dump_data(post)}



class Post(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()


    @jwt_required()
    def get(self, id: int):
        post = self.post_service.find_by_id(id)
        if not post:
            raise UNotFound("post id not found")

        return {'data': SerializerPost().dump_data(post)}



class Comments(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.comment_service = CommentService()


    @jwt_required()
    @validate_body(CommentsRequestSchema)
    def post(self, post_id: int):
        account_user_id = current_user.id

        post = self.post_service.first(id=post_id, account_user_id=account_user_id)
        if not post:
            raise UNotFound("post id not found")

        body = self.body

        comment_reply = None
        if body.get('reply_id'):
            comment_reply = self.comment_service.first(id=body.get('reply_id'), post_id=post_id)

            if not comment_reply:
                raise UNotFound("comment id not found")

        with session_scope():
            self.comment_service.create(**self.body, account_user_id=account_user_id, post_id=post_id)
            self.post_service.update(post, comment_count=post.comment_count + 1)
            if comment_reply:
                self.comment_service.update(comment_reply, reply_count=comment_reply.reply_count + 1)

            return {'message': "Created successfully"}
