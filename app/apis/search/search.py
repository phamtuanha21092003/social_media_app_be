from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.services.validators import get_limit_from_page, validate_params
from app.services.models.account_user import AccountUserService
from app.services.models.post import PostService
from app.services.validators.search import SearchSchema
from app.services.serializers.account_user import SerializerAccountUser
from app.services.serializers.post import SerializerPost



class Search(Resource):
    def __init__(self):
        self.account_user_service = AccountUserService()
        self.post_service = PostService()


    @jwt_required()
    @validate_params(SearchSchema)
    def get(self):
        params = self.params

        limit, offset = get_limit_from_page(params)

        type = params.get('type', 'ALL')

        users = []
        total_users = 0

        posts = []
        total_posts = 0

        keyword = params.get('keyword')

        if type == "ALL" or type == "PEOPLE":
            users, total_users = self.account_user_service.get_users_by_keyword(keyword, limit, offset)
            users = SerializerAccountUser(many=True).dump(users)

        if type == "ALL" or type == "POST":
            posts, total_posts = self.post_service.get_posts_by_keyword(keyword, limit, offset)
            posts = SerializerPost(many=True, exclude=["comments"]).dump_data(posts)

        return {
            "message": "success",
            "users": {
                "total": total_users,
                "data": users
            },
            "posts": {
                "total": total_posts,
                "data": posts
            }
        }