from marshmallow import fields, Schema


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    id = fields.UUID(required=True)
