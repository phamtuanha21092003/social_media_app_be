from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.comment import CommentService
from app.services.models.post import PostService
from app.services.models import AccountUserService
from app.services.models.post_like import PostLikeService
from app.services.models.post_save import PostSaveService
from app.services.serializers.post import SerializerPost
from app.services.validators import get_limit_from_page, validate_body, validate_params, PagingSchema
from app.services.validators.feed import CreatePostRequestSchema, GetPostsRequestSchema, UpadatePostRequestSchema
from app.services.validators.feed.post import CommentsRequestSchema
from db import session_scope
from app.common.errors import UNotFound



class Posts(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.account_user_service = AccountUserService()


    @jwt_required()
    @validate_params(GetPostsRequestSchema)
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
            if user_id == current_user.id:
                kwargs.update({'account_user_id': user_id, 'status': ['ACTIVE', 'PRIVATE']})

            else:
                user = self.account_user_service.find_by_id(user_id)
                if not user:
                    raise UNotFound("User not found")

                kwargs.update({'account_user_id': user_id, 'status': 'ACTIVE'})

        else:
            kwargs.update({'status': 'ACTIVE'})

        posts, total = self.post_service.find(**kwargs)

        return {"total": total, "data": SerializerPost(many=True, exclude=["comments"]).dump_data(posts)}


    @jwt_required()
    @validate_body(CreatePostRequestSchema)
    def post(self):
        with session_scope():
            kwargs = {
                'title': self.body.get("title"),
                'url': self.body.get("url"),
            }

            if self.body.get("is_private"):
                kwargs.update({"status": "PRIVATE"})

            post = self.post_service.create(account_user_id=current_user.id, **kwargs)

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


    @jwt_required()
    @validate_body(UpadatePostRequestSchema)
    def put(self, id: int):
        user_id = current_user.id

        post = self.post_service.find_by_id(id)

        if post.account_user_id != user_id:
            raise UNotFound("post id not found")

        data = {}

        if self.body.get("title"):
            data["title"] = self.body['title']

        if self.body.get("url"):
            data["url"] = self.body['url']

        if self.body.get("status"):
            data["status"] = self.body['status']

        with session_scope():
            self.post_service.update(post, **data)

            return {"message": "success", "status": post.status}



class Comments(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.comment_service = CommentService()


    @jwt_required()
    @validate_body(CommentsRequestSchema)
    def post(self, post_id: int):
        account_user_id = current_user.id

        post = self.post_service.first(id=post_id)
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



class PostLike(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.account_user_service = AccountUserService()
        self.post_like_service = PostLikeService()


    @jwt_required()
    def post(self, post_id: int):
        user_id = current_user.id

        post = self.post_service.find_by_id(post_id)
        if not post:
            raise UNotFound("post id not found")

        post_like = self.post_like_service.first(post_id=post_id, account_user_id=user_id)

        with session_scope():
            if not post_like:
                self.post_like_service.create(account_user_id=user_id, post_id=post_id)
                post = self.post_service.update(post, like_count=post.like_count + 1)
                return {'message': "success", "is_liked": True, "like_count": post.like_count}

            self.post_like_service.delete(post_like)
            post = self.post_service.update(post, like_count=post.like_count - 1)
            return {'message': "success", "is_liked": False, "like_count": post.like_count}



class PostLiked(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.post_like_service = PostLikeService()


    @jwt_required()
    @validate_params(PagingSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        post_likes, total = self.post_like_service.find(account_user_id=user_id, order_bys=[self.post_like_service.model.created.desc()], limit=limit, offset=offset, is_get_total=True)
        post_ids = [post.post_id for post in post_likes]

        posts = self.post_service.find(id=post_ids)

        return {'data': SerializerPost(many=True, exclude=["comments"]).dump_data(posts), 'total': total, 'message': 'success'}



class PostSave(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.account_user_service = AccountUserService()
        self.post_save_service = PostSaveService()


    @jwt_required()
    def post(self, post_id: int):
        user_id = current_user.id

        post = self.post_service.find_by_id(post_id)
        if not post:
            raise UNotFound("post id not found")

        post_save = self.post_save_service.first(post_id=post_id, account_user_id=user_id)

        with session_scope():
            if not post_save:
                self.post_save_service.create(account_user_id=user_id, post_id=post_id)
                return {'message': "success", "is_saved": True}

            self.post_save_service.delete(post_save)
            return {'message': "success", "is_saved": False}



class PostSaved(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()
        self.post_save_service = PostSaveService()


    @jwt_required()
    @validate_params(PagingSchema)
    def get(self):
        user_id = current_user.id

        limit, offset = get_limit_from_page(self.params)

        post_saves, total = self.post_save_service.find(account_user_id=user_id, order_bys=[self.post_save_service.model.created.desc()], limit=limit, offset=offset, is_get_total=True)
        post_ids = [post.post_id for post in post_saves]

        posts = self.post_service.find(id=post_ids)

        return {'data': SerializerPost(many=True, exclude=["comments"]).dump_data(posts), 'total': total, 'message': 'success'}

