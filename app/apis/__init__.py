from flask import Blueprint
from .auth import *
from .uploads import *
from .profile import *
from .feed import *
from .search import *
from .chat import *

api_blueprint = Blueprint("api_blueprint", __name__, url_prefix="/apis")


api_blueprint.register_blueprint(auth_blueprint)
api_blueprint.register_blueprint(upload_blueprint)
api_blueprint.register_blueprint(profile_blueprint)
api_blueprint.register_blueprint(feed_blueprint)
api_blueprint.register_blueprint(search_blueprint)
api_blueprint.register_blueprint(chat_blueprint)
