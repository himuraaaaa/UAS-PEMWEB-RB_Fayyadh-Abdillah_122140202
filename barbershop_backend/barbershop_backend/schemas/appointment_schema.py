from marshmallow import Schema, fields, validate

class AppointmentCreateSchema(Schema):
    barber_id = fields.Int(required=True, validate=validate.Range(min=1))
    service_id = fields.Int(required=True, validate=validate.Range(min=1))
    appointment_date = fields.DateTime(required=True)
    notes = fields.Str(allow_none=True)
    # user_id tidak disertakan di sini karena diambil dari token JWT

class AppointmentUpdateSchema(Schema):
    barber_id = fields.Int(validate=validate.Range(min=1))
    service_id = fields.Int(validate=validate.Range(min=1))
    appointment_date = fields.DateTime()
    notes = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'confirmed', 'completed', 'cancelled'])) 