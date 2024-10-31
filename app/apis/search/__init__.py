from flask import Blueprint
from flask_restful import Api
from .search import Search

search_blueprint = Blueprint("search_blueprint", __name__, url_prefix="/search")
search_api = Api(search_blueprint)


search_resources = {
    "/": Search
}


for url_path, view in search_resources.items():
    search_api.add_resource(
        view, '{}/'.format(url_path)
    )
