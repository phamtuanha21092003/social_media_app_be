from marshmallow import RAISE, ValidationError, fields, validates
from .. import BaseSchema, PagingSchema



class GetFriendsRequestSchema(PagingSchema):
    keyword = fields.Str()



class UpdateProfileRequestSchema(BaseSchema):
    class Meta:
        unknown = RAISE

    name = fields.Str()
    phone = fields.Str()
    address = fields.Str()
    avatar = fields.Str()


    @validates('avatar')
    def validate_image(self, image):
        if image and not image.startswith('http://localhost:9000/wey-bucket/files/'):
            raise ValidationError('{} must be upload to min io'.format(image))

        return True