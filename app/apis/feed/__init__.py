from flask import Blueprint
from flask_restful import Api
from .post import Post


feed_blueprint = Blueprint("post_blueprint", __name__, url_prefix="/feed")
feed_api = Api(feed_blueprint)


feed_resources = {
    "/posts": Post,
}


for url_path, view in feed_resources.items():
    feed_api.add_resource(
        view, '{}/'.format(url_path)
    )
