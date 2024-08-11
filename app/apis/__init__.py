from flask import Blueprint
from .auth import *
from .uploads import *


api_blueprint = Blueprint("api_blueprint", __name__, url_prefix="/apis")


api_blueprint.register_blueprint(auth_blueprint)
api_blueprint.register_blueprint(upload_blueprint)