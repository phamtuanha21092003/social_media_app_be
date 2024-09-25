from flask import Blueprint
from flask_restful import Api


account_blueprint = Blueprint('account', __name__, url_prefix='/account')
account_api = Api(account_blueprint)


account_routers = {

}

for url_path, view in account_routers.items():
    account_api.add_resource(
        view, '{}/'.format(url_path)
    )
