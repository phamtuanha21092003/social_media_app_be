import functools
import re
from typing import Type
from flask import request
from marshmallow import EXCLUDE, Schema, fields
from app.common.errors import UBadRequest



class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE



class PagingSchema(BaseSchema):
    page = fields.Integer()
    per_page = fields.Integer()



def validate_body(validate_schema: Type[BaseSchema], is_many=False):

    def is_form(content_type: str):
        return (
            ('application/x-www-form-urlencoded' in content_type)
            or ('multipart/form-data' in content_type)
        )


    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            content_type = request.headers.get('Content-Type', '')

            if is_form(content_type):
                self.body = validate_schema().load(request.form)

            else:
                self.body = validate_schema(many=is_many).load(request.get_json(force=True))

            return func(*args, **kwargs)

        return wrapper

    return decorator



def validate_params(validate_schema: Type[BaseSchema]):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            params = request.args.to_dict()

            for key in params.keys():
                if key[-2:] == '[]':
                    params[key[:-2]] = request.args.getlist(key)
                    params.pop(key, None)

            self.params = validate_schema().load(params)

            return func(*args, **kwargs)

        return wrapper

    return decorator



def get_limit_from_page(params: dict) -> tuple[int, int]:
    try:
        page = int(params.get('page', 1))
        per_page = int(params.get('per_page', 10))
    except Exception:
        raise UBadRequest('Invalid limit or offset')
    limit = per_page
    offset = (page - 1) * per_page
    if limit > 100 or limit < 0:
        raise UBadRequest('Limit invalid. Maximum limit is 100')
    if offset < 0:
        raise UBadRequest('Page info invalid')
    return limit, offset
