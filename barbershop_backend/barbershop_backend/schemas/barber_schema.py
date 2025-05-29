from marshmallow import Schema, fields, validate, ValidationError

class BarberSchema(Schema):
    """Schema for Barber validation"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    position = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    image = fields.Str(required=True)
    social = fields.Dict(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        strict = True

class BarberUpdateSchema(Schema):
    """Schema for Barber update validation"""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    position = fields.Str(validate=validate.Length(min=2, max=100))
    image = fields.Str()
    social = fields.Dict(allow_none=True)

    class Meta:
        strict = True 