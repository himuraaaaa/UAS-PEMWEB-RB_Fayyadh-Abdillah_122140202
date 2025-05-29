from marshmallow import Schema, fields, validate, ValidationError

class ServiceSchema(Schema):
    """Schema for Service validation"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(required=True, validate=validate.Length(max=500))
    duration = fields.Int(required=True)  # Duration in minutes
    price = fields.Float(required=True, validate=validate.Range(min=0))
    image = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        strict = True

class ServiceUpdateSchema(Schema):
    """Schema for Service update validation"""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    duration = fields.Int()
    price = fields.Float(validate=validate.Range(min=0))
    image = fields.Str()

    class Meta:
        strict = True 