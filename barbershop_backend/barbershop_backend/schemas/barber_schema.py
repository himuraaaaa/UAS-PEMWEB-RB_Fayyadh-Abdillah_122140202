from marshmallow import Schema, fields, validate, ValidationError

class BarberSchema(Schema):
    """Schema for Barber validation"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Regexp(r'^\+?1?\d{9,15}$'))
    bio = fields.Str(validate=validate.Length(max=500))
    rating = fields.Float(validate=validate.Range(min=0, max=5))
    is_available = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        strict = True

class BarberUpdateSchema(Schema):
    """Schema for Barber update validation"""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    phone = fields.Str(validate=validate.Regexp(r'^\+?1?\d{9,15}$'))
    bio = fields.Str(validate=validate.Length(max=500))
    is_available = fields.Bool()

    class Meta:
        strict = True 