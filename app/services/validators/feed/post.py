from app.services.validators import BaseSchema
from marshmallow import fields, validate


class CommentsPostRequestSchema(BaseSchema):
    title = fields.Str(required=True, allow_none=False, validate=validate.Length(min=1))
    reply_id = fields.Integer(allow_none=True)



class CommentsPutRequestSchema(BaseSchema):
    title = fields.Str(required=True, allow_none=False, validate=validate.Length(min=1))
    id = fields.Integer(required=True)



class CommentsDeleteRequestSchema(BaseSchema):
    id = fields.Integer(required=True)



class UpdateEmojiRequestSchema(BaseSchema):
    post_id = fields.Integer(required=True)
    emoji_id = fields.Integer(required=True, validate=validate.OneOf({21, 31, 32, 33, 34}))



class DeleteEmojiRequestSchema(BaseSchema):
    post_id = fields.Integer(required=True)

