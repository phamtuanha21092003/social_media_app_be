from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.models.post import PostService
from app.services.serializers.post import SerializerPost
from app.services.validators import PagingSchema, get_limit_from_page, validate_body, validate_params
from app.services.validators.feed import CreatePostRequest
from db import session_scope


class Post(Resource):
    def __init__(self) -> None:
        self.post_service = PostService()


    @jwt_required()
    @validate_params(PagingSchema)
    def get(self):
        limit, offset = get_limit_from_page(self.params)

        posts, total = self.post_service.find(limit=limit, offset=offset, is_get_total=True, account_user_id=current_user.id)

        return { "total": total, "data": SerializerPost(many=True, exclude=["comments"]).dump_data(posts) }


    @jwt_required()
    @validate_body(CreatePostRequest)
    def post(self):
        with session_scope():
            self.post_service.create(account_user_id=current_user.id, **self.body)

            return { 'message': 'Created successfully' }
