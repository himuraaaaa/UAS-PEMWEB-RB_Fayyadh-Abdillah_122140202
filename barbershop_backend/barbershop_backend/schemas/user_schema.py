from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    """Schema for User validation"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)
    is_admin = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        strict = True

class UserLoginSchema(Schema):
    """Schema for User login validation"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    class Meta:
        strict = True

class UserUpdateSchema(Schema):
    """Schema for User update validation"""
    username = fields.Str(validate=validate.Length(min=3, max=50))
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=6), load_only=True)

    class Meta:
        strict = True 