from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class UserSchema(Schema):
    """Schema for User validation"""
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, allow_none=False, validate=validate.Length(min=8), load_only=True)
    confirm_password = fields.Str(required=True, allow_none=False, validate=validate.Length(min=8), load_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone_number = fields.Str(validate=validate.Length(max=20), allow_none=True)
    is_admin = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        strict = True

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        if not data.get('password') or not data.get('confirm_password'):
            raise ValidationError('Password and confirm_password are required', field_name='confirm_password')
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError('Passwords do not match', field_name='confirm_password')

class UserLoginSchema(Schema):
    """Schema for User login validation"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    class Meta:
        strict = True

class UserUpdateSchema(Schema):
    """Schema for User update validation"""
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=8), load_only=True)
    first_name = fields.Str(validate=validate.Length(min=1, max=50))
    last_name = fields.Str(validate=validate.Length(min=1, max=50))
    phone_number = fields.Str(validate=validate.Length(max=20))

    class Meta:
        strict = True 