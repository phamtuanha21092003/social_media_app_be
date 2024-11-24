from marshmallow import ValidationError, fields, validates, validate
from app.services.validators import BaseSchema, PagingSchema


class CreatePostRequestSchema(BaseSchema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    url = fields.Str(allow_none=True)
    is_private = fields.Bool(allow_none=True)

    @validates('url')
    def validate_image(self, image):
        if image and not image.startswith('http://localhost:9000/wey-bucket/files/'):
            raise ValidationError('{} must be upload to min io'.format(image))

        return True



class GetPostsRequestSchema(PagingSchema):
    user_id = fields.Int()



class UpadatePostRequestSchema(BaseSchema):
    status = fields.Str(validate=validate.OneOf(['ACTIVE', 'DELETED', 'PRIVATE']), allow_none=True)
    title = fields.Str(validate=validate.Length(min=1), allow_none=True)
    url = fields.Str(allow_none=True)

    @validates('url')
    def validate_image(self, image):
        if image and not image.startswith('http://localhost:9000/wey-bucket/files/'):
            raise ValidationError('{} must be upload to min io'.format(image))

        return True
