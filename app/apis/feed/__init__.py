from flask import Blueprint
from flask_restful import Api
from .posts import Posts, Post, Comments, PostLike, PostLiked, PostSave, PostSaved

feed_blueprint = Blueprint("feed_blueprint", __name__, url_prefix="/feed")
feed_api = Api(feed_blueprint)


feed_resources = {
    "/posts": Posts,
    "/post/<int:id>": Post,
    "/comments/<int:post_id>": Comments,
    "/posts/like/<int:post_id>": PostLike,
    "/posts/liked": PostLiked,
    "/posts/save/<int:post_id>": PostSave,
    "/posts/saved": PostSaved
}


for url_path, view in feed_resources.items():
    feed_api.add_resource(
        view, '{}/'.format(url_path)
    )
