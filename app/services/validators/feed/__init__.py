from marshmallow import ValidationError, fields, validates
from app.services.validators import BaseSchema


class CreatePostRequest(BaseSchema):
    title = fields.Str(required=True)
    url = fields.Str(allow_none=True)

    @validates('url')
    def validate_image(self, image):
        if image and not image.startswith('http://localhost:9000/wey-bucket/files/'):
            raise ValidationError('{} must be upload to min io'.format(image))

        return True