from marshmallow import RAISE, ValidationError, fields, validates, validate
from .. import BaseSchema, PagingSchema
from models.account_friendship import Status


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



class ConfirmFriendShipPostRequestSchema(BaseSchema):
    creator_id = fields.Integer(required=True, allow_none=False)



class FriendshipGetRequestSchema(PagingSchema):
    status = fields.List(fields.Str(allow_none=True, validate=validate.OneOf(Status.__args__)), allow_none=False)
    keyword = fields.Str()



class DeleteFriendShipRequestSchema(BaseSchema):
    creator_id = fields.Integer(required=True, allow_none=False)
