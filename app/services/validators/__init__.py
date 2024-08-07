import functools
from typing import Type
from flask import request
from marshmallow import EXCLUDE, Schema, fields



class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

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