from app.services.validators import BaseSchema
from marshmallow import fields, validates_schema, ValidationError


class ChangePasswordRequestSchema(BaseSchema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_password(self, data, **kwargs):
        if data["old_password"] == data["new_password"]:
            raise ValidationError("Password cannot be the same.")

        if data['new_password'] != data['confirm_password']:
            raise ValidationError("Passwords do not match.")
