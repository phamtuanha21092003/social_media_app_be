from flask import Blueprint
from flask_restful import Api
from .login import Login
from .sign_up import SignUp
from .refresh import Refresh
from .logout import Logout


auth_blueprint = Blueprint("auth_blueprint", __name__, url_prefix="/auth")
auth_api = Api(auth_blueprint)


auth_routers = {
    "/login": Login,
    "/sign_up": SignUp,
    "/refresh": Refresh,
    '/logout': Logout,
}


for url_path, view in auth_routers.items():
    auth_api.add_resource(
        view, '{}/'.format(url_path)
    )
