from marshmallow import fields, validate
from app.services.validators import PagingSchema
import enum



class TYPE_SEARCH(enum.Enum):
    ALL = "ALL"
    PEOPLE = "PEOPLE"
    POST = "POST"



class SearchSchema(PagingSchema):
    type = fields.Str(validate=validate.OneOf(TYPE_SEARCH), missing="ALL")
    keyword = fields.Str(required=True)
