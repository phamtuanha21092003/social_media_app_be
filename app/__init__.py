from flask import Flask
from config import Config
from db import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import select
from models import AccountUser
import json
from .common.errors import (
    UPermissionDenied,
    UNotFound,
    UUnprocessableEntity,
    UConflict,
    UBadRequest,
    UForbidden
)
from ratelimit import RateLimitException
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


jwt = JWTManager()


def create_app(config=Config()):
    app = Flask(__name__)

    app.config.from_object(config)

    __init_extensions(app)

    __config_error_handlers(app)

    __config_blueprints(app)

    return app



def __init_extensions(app: Flask):
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)


    @jwt.user_identity_loader
    def user_identity_lookup(account_user):
        return account_user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db.session.execute(select(AccountUser).filter_by(id=identity)).scalar_one()


def __config_blueprints(app: Flask):
    from .apis import api_blueprint
    app.register_blueprint(api_blueprint)


def __config_error_handlers(app: Flask):
    @app.errorhandler(RateLimitException)
    def rate_limit_error_handler(error):
        # TODO: Should change the error message format in future
        return (
            {'error': 'Too many request'},
            429,
        )

    @app.errorhandler(ValidationError)
    def validation_error_handler(error):
        # TODO: Should change the error message format in future
        return (
            {'error': 'Bad request', 'messages': error.messages},
            400,
        )

    @app.errorhandler(500)
    def server_error_page(error):
        return {'error': 'Internal server error'}, 500

    @app.errorhandler(UForbidden)
    def forbidden(error):
        return {'error': str(error) or 'Forbidden'}, 403

    @app.errorhandler(UConflict)
    def conflict(error):
        return {'error': str(error) or 'Conflict'}, 409

    @app.errorhandler(404)
    def page_not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(UPermissionDenied)
    def permission_denied(error):
        return {'error': str(error)}, 401

    @app.errorhandler(UNotFound)
    def not_found(error):
        error_message = str(error) or 'Resource not found'
        return {'error': error_message}, 404

    @app.errorhandler(UUnprocessableEntity)
    def unprocessable_entity(error):
        error_message = str(error) or 'Unprocessable Entity'
        return {'error': error_message}, 422

    @app.errorhandler(UBadRequest)
    def bad_request(error):
        error_message = str(error) or 'Bad Request'
        return {'error': error_message}, 400

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        error_message = str(error) or 'Integrity Error'
        return {'error': error_message}, 500