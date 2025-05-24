from marshmallow import Schema, fields, validate, ValidationError

class ServiceSchema(Schema):
    """Schema for Service validation"""
    # Existing fields...
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    duration = fields.Int() # Duration in minutes
    price = fields.Float(required=True, validate=validate.Range(min=0))
    barber_id = fields.Int(required=True, load_only=True)

    class Meta:
        strict = True

class ServiceUpdateSchema(Schema):
    """Schema for Service update validation"""
    name = fields.Str(validate=validate.Length(min=2, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    duration = fields.Int()
    price = fields.Float(validate=validate.Range(min=0))
    barber_id = fields.Int(load_only=True)

    class Meta:
        strict = True 