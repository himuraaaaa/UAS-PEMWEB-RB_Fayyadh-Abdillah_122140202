from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest, HTTPForbidden, HTTPInternalServerError
from sqlalchemy.exc import SQLAlchemyError
from ..orms import User, Barber, Service, Appointment
from ..schemas.user_schema import UserSchema, UserLoginSchema
from ..schemas.barber_schema import BarberSchema, BarberUpdateSchema
from ..schemas.service_schema import ServiceUpdateSchema, ServiceSchema
from ..schemas.appointment_schema import AppointmentCreateSchema, AppointmentUpdateSchema
from ..utils.validation import validate_request
from datetime import datetime
import json
import logging
from marshmallow import ValidationError
import os
from ..utils.jwt import require_jwt

log = logging.getLogger(__name__)

# Authentication Views
@view_config(route_name='api.auth.login', renderer='json', request_method='POST')
def login(request):
    # Validate request data
    schema = UserLoginSchema()
    data, error = validate_request(schema, request)
    if error:
        return error

    try:
        log.info(f"Attempting login for email: {data['email']}")
        user = request.dbsession.query(User).filter_by(email=data['email']).first()
        
        if not user:
            log.warning(f"No user found with email: {data['email']}")
            return {'status': 'error', 'message': 'Invalid credentials'}
            
        if user.check_password(data['password']):
            log.info(f"Login successful for user: {user.username}")
            
            # Generate JWT token
            token = request.jwt_manager.create_token(
                user_id=user.id,
                username=user.username,
                is_admin=user.is_admin
            )
            
            return {
                'status': 'success',
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            }
            
        log.warning(f"Invalid password for user: {user.username}")
        return {'status': 'error', 'message': 'Invalid credentials'}
    except Exception as e:
        log.error(f"Login error: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.auth.login', request_method='OPTIONS', renderer='json')
def login_options(request):
    return {}

@view_config(route_name='api.auth.register', renderer='json', request_method='POST')
def register(request):
    try:
        # Validate request data
        schema = UserSchema()
        data, error = validate_request(schema, request)
        if error:
            return error

        log.info(f"Attempting to register user with email: {data['email']}")
        
        # Check if user already exists
        existing_user = request.dbsession.query(User).filter_by(email=data['email']).first()
        if existing_user:
            log.warning(f"Registration failed: Email {data['email']} already registered")
            return {'status': 'error', 'message': 'Email already registered'}

        # Create new user
        user = User(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data.get('phone_number')
        )
        request.dbsession.add(user)
        request.dbsession.commit()
        
        log.info(f"Successfully registered user: {user.email} with ID: {user.id}")
        return {
            'status': 'success',
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number
            }
        }
    except SQLAlchemyError as e:
        log.error(f"Database error during registration: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'Database error occurred'}
    except ValueError as e:
        log.error(f"Validation error during registration: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        log.error(f"Unexpected error during registration: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An unexpected error occurred'}

@view_config(route_name='api.auth.register', request_method='OPTIONS', renderer='json')
def register_options(request):
    return {}

# Barber Views
@view_config(route_name='api.barbers', renderer='json', request_method='GET')
def get_barbers(request):
    try:
        barbers = request.dbsession.query(Barber).all()
        schema = BarberSchema(many=True)
        return {'status': 'success', 'data': schema.dump(barbers)}
    except Exception as e:
        log.error(f"Error fetching barbers: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.barber', renderer='json', request_method='GET')
def get_barber(request):
    try:
        barber_id = request.matchdict['id']
        barber = request.dbsession.query(Barber).get(barber_id)
        if not barber:
            return HTTPNotFound()
        schema = BarberSchema()
        return {'status': 'success', 'data': schema.dump(barber)}
    except Exception as e:
        log.error(f"Error fetching barber: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.barber.create', renderer='json', request_method='POST')
def create_barber(request):
    # Check if user is admin from JWT payload
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to create barber")
        raise HTTPForbidden('Admin access required')

    schema = BarberSchema()
    data, error = validate_request(schema, request)
    if error:
        return error

    try:
        log.info(f"Attempting to create barber with name: {data['name']}")
        barber = Barber(
            name=data['name'],
            position=data['position'],
            image=data['image'],
            social=data.get('social')
        )
        request.dbsession.add(barber)
        request.dbsession.commit()
        log.info(f"Successfully created barber with ID: {barber.id}")
        return {'status': 'success', 'barber_id': barber.id}
    except SQLAlchemyError as e:
        log.error(f"Database error during barber creation: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'Database error occurred'}
    except Exception as e:
        log.error(f"Unexpected error during barber creation: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An unexpected error occurred'}

@view_config(route_name='api.barber.update', renderer='json', request_method='PUT')
def update_barber(request):
    # Check if user is admin from JWT payload
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to update barber")
        raise HTTPForbidden('Admin access required')

    barber_id = request.matchdict.get('id')
    if not barber_id:
        raise HTTPBadRequest('Barber ID is required')

    try:
        barber = request.dbsession.query(Barber).get(barber_id)
        if not barber:
            raise HTTPNotFound('Barber not found')

        schema = BarberUpdateSchema()
        data, error = validate_request(schema, request)
        if error:
            return error

        for key, value in data.items():
            setattr(barber, key, value)

        request.dbsession.commit()
        log.info(f"Successfully updated barber with ID: {barber_id}")
        return {'status': 'success', 'message': 'Barber updated successfully'}

    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error updating barber {barber_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while updating the barber'}

@view_config(route_name='api.barber.delete', renderer='json', request_method='DELETE')
def delete_barber(request):
    # Check if user is admin from JWT payload
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to delete barber")
        raise HTTPForbidden('Admin access required')

    barber_id = request.matchdict.get('id')
    if not barber_id:
        raise HTTPBadRequest('Barber ID is required')

    try:
        barber = request.dbsession.query(Barber).get(barber_id)
        if not barber:
            raise HTTPNotFound('Barber not found')

        request.dbsession.delete(barber)
        request.dbsession.commit()
        log.info(f"Successfully deleted barber with ID: {barber_id}")
        return {'status': 'success', 'message': 'Barber deleted successfully'}

    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error deleting barber {barber_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while deleting the barber'}

# Service Views
@view_config(route_name='api.services', renderer='json', request_method='GET')
def get_services(request):
    try:
        services = request.dbsession.query(Service).all()
        schema = ServiceSchema(many=True)
        return {'status': 'success', 'data': schema.dump(services)}
    except Exception as e:
        log.error(f"Error fetching services: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.service', renderer='json', request_method='GET')
def get_service(request):
    try:
        service_id = request.matchdict.get('id')
        if not service_id:
            raise HTTPBadRequest('Service ID is required')

        service = request.dbsession.query(Service).get(service_id)
        if not service:
            raise HTTPNotFound('Service not found')

        schema = ServiceSchema()
        return {'status': 'success', 'data': schema.dump(service)}
    except HTTPNotFound:
        raise
    except HTTPBadRequest:
        raise
    except Exception as e:
        log.error(f"Error fetching service: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.service.create', renderer='json', request_method='POST')
def create_service(request):
    # Check if user is admin from JWT payload
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to create service")
        raise HTTPForbidden('Admin access required')

    schema = ServiceSchema()
    data, error = validate_request(schema, request)
    if error:
        return error

    try:
        log.info(f"Attempting to create service with name: {data['name']}")
        service = Service(
            name=data['name'],
            description=data['description'],
            duration=data['duration'],
            price=data['price'],
            image=data['image']
        )
        request.dbsession.add(service)
        request.dbsession.commit()
        log.info(f"Successfully created service with ID: {service.id}")
        return {'status': 'success', 'service_id': service.id}
    except SQLAlchemyError as e:
        log.error(f"Database error during service creation: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'Database error occurred'}
    except Exception as e:
        log.error(f"Unexpected error during service creation: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An unexpected error occurred'}

@view_config(route_name='api.service.update', renderer='json', request_method='PUT')
def update_service(request):
    # Check if user is admin from JWT payload
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to update service")
        raise HTTPForbidden('Admin access required')

    service_id = request.matchdict.get('id')
    if not service_id:
        raise HTTPBadRequest('Service ID is required')

    try:
        service = request.dbsession.query(Service).get(service_id)
        if not service:
            raise HTTPNotFound('Service not found')

        schema = ServiceUpdateSchema()
        data, error = validate_request(schema, request)
        if error:
            return error

        for key, value in data.items():
            if hasattr(service, key):
                setattr(service, key, value)

        request.dbsession.commit()
        log.info(f"Successfully updated service with ID: {service_id}")
        return {'status': 'success', 'message': 'Service updated successfully'}
    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error updating service {service_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while updating the service'}

@view_config(route_name='api.service.delete', renderer='json', request_method='DELETE')
def delete_service(request):
    # Check if user is admin from JWT payload
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to delete service")
        raise HTTPForbidden('Admin access required')

    service_id = request.matchdict.get('id')
    if not service_id:
        raise HTTPBadRequest('Service ID is required')

    try:
        service = request.dbsession.query(Service).get(service_id)
        if not service:
            raise HTTPNotFound('Service not found')

        request.dbsession.delete(service)
        request.dbsession.commit()
        log.info(f"Successfully deleted service with ID: {service_id}")
        return {'status': 'success', 'message': 'Service deleted successfully'}
    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error deleting service {service_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while deleting the service'}

# Appointment Views
@view_config(route_name='api.appointments', renderer='json', request_method='GET')
def get_appointments(request):
    try:
        if not request.jwt.get('is_admin', False):
            appointments = request.dbsession.query(Appointment).filter_by(user_id=request.jwt['user_id']).all()
        else:
            appointments = request.dbsession.query(Appointment).all()
        # Kembalikan dengan .to_dict() agar field user_id selalu ada
        return {'status': 'success', 'data': [apt.to_dict() for apt in appointments]}
    except Exception as e:
        log.error(f"Error getting appointments: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.appointment.create', renderer='json', request_method='POST')
def create_appointment(request):
    schema = AppointmentCreateSchema()
    data, error = validate_request(schema, request)
    if error:
        return error

    try:
        log.info(f"Received data for appointment creation: {data}")
        appointment = Appointment(
            user_id=request.jwt['user_id'],
            barber_id=data['barber_id'],
            service_id=data['service_id'],
            appointment_date=data['appointment_date'],
            notes=data.get('notes')
        )
        request.dbsession.add(appointment)
        request.dbsession.commit()
        log.info(f"Successfully created appointment with ID: {appointment.id}")
        return {'status': 'success', 'appointment_id': appointment.id}
    except SQLAlchemyError as e:
        log.error(f"Database Error creating appointment: {type(e).__name__} - {str(e)}")
        request.dbsession.rollback()
        raise HTTPInternalServerError({
            'status': 'error',
            'message': 'Database error occurred while creating the appointment'
        })
    except Exception as e:
        log.error(f"Truly Unexpected Error creating appointment after validation: {type(e).__name__} - {str(e)}")
        request.dbsession.rollback()
        raise HTTPInternalServerError({
            'status': 'error',
            'message': 'An unexpected error occurred during appointment creation process'
        })

@view_config(route_name='api.appointment.update', renderer='json', request_method='PUT')
def update_appointment(request):
    appointment_id = request.matchdict.get('id')
    if not appointment_id:
        raise HTTPBadRequest('Appointment ID is required')

    try:
        appointment = request.dbsession.query(Appointment).get(appointment_id)
        if not appointment:
            raise HTTPNotFound('Appointment not found')

        if not request.jwt.get('is_admin', False) and appointment.user_id != request.jwt['user_id']:
            log.warning(f"Unauthorized attempt to update appointment {appointment_id}")
            raise HTTPForbidden('You can only update your own appointments')

        schema = AppointmentUpdateSchema()
        data, error = validate_request(schema, request)
        if error:
            return error

        for key, value in data.items():
            if hasattr(appointment, key):
                setattr(appointment, key, value)

        request.dbsession.commit()
        log.info(f"Successfully updated appointment with ID: {appointment_id}")
        return {'status': 'success', 'message': 'Appointment updated successfully'}

    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except HTTPForbidden:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error updating appointment {appointment_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while updating the appointment'}

@view_config(route_name='api.appointment.delete', renderer='json', request_method='DELETE')
def delete_appointment(request):
    appointment_id = request.matchdict.get('id')
    if not appointment_id:
        raise HTTPBadRequest('Appointment ID is required')

    try:
        appointment = request.dbsession.query(Appointment).get(appointment_id)
        if not appointment:
            raise HTTPNotFound('Appointment not found')

        if not request.jwt.get('is_admin', False) and appointment.user_id != request.jwt['user_id']:
            log.warning(f"Unauthorized attempt to delete appointment {appointment_id}")
            raise HTTPForbidden('You can only delete your own appointments')

        request.dbsession.delete(appointment)
        request.dbsession.commit()
        log.info(f"Successfully deleted appointment with ID: {appointment_id}")
        return {'status': 'success', 'message': 'Appointment deleted successfully'}

    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except HTTPForbidden:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error deleting appointment {appointment_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while deleting the appointment'}

@view_config(route_name='api.appointment', renderer='json', request_method='GET')
def get_appointment(request):
    appointment_id = request.matchdict.get('id')
    if not appointment_id:
        raise HTTPBadRequest('Appointment ID is required')

    try:
        appointment = request.dbsession.query(Appointment).get(appointment_id)
        if not appointment:
            raise HTTPNotFound('Appointment not found')

        if not request.jwt.get('is_admin', False) and appointment.user_id != request.jwt['user_id']:
            log.warning(f"Unauthorized attempt to view appointment {appointment_id}")
            raise HTTPForbidden('You can only view your own appointments')

        schema = AppointmentCreateSchema()
        return {'status': 'success', 'data': schema.dump(appointment)}

    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except HTTPForbidden:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error retrieving appointment {appointment_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while retrieving the appointment'}

@view_config(route_name='api.appointment.update_status', renderer='json', request_method='PUT')
def update_appointment_status(request):
    # Check if user is admin from JWT payload
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to update appointment status")
        raise HTTPForbidden('Admin access required to update appointment status')

    appointment_id = request.matchdict.get('id')
    if not appointment_id:
        raise HTTPBadRequest('Appointment ID is required')

    try:
        data = request.json_body
        new_status = data.get('status')
        if not new_status:
            raise HTTPBadRequest('New status is required in the request body')

        appointment = request.dbsession.query(Appointment).get(appointment_id)
        if not appointment:
            raise HTTPNotFound('Appointment not found')

        appointment.status = new_status
        request.dbsession.commit()
        
        log.info(f"Successfully updated status for appointment ID: {appointment_id} to '{new_status}'")
        return {'status': 'success', 'message': 'Appointment status updated successfully'}

    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except HTTPForbidden:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error updating appointment status {appointment_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while updating the appointment status'}

@view_config(route_name='api.upload', renderer='json', request_method='POST')
@require_jwt
def upload_file(request):
    try:
        # Check if file is in request
        if 'file' not in request.POST:
            return {'status': 'error', 'message': 'No file uploaded'}

        file = request.POST['file'].file
        filename = request.POST['file'].filename

        # Validate file extension
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            return {'status': 'error', 'message': 'Invalid file format. Only JPG, JPEG, and PNG are allowed'}

        # Create assets/barbers directory if it doesn't exist
        upload_dir = os.path.join('barbershop_backend', 'barbershop_backend', 'assets', 'barbers')
        os.makedirs(upload_dir, exist_ok=True)

        # Save file
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(file.read())

        return {'status': 'success', 'filename': filename}
    except Exception as e:
        log.error(f"Error uploading file: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.users', renderer='json', request_method='GET')
def get_users(request):
    # Hanya admin yang boleh akses
    if not request.jwt.get('is_admin', False):
        log.warning(f"Unauthorized attempt to fetch all users")
        raise HTTPForbidden('Admin access required')
    try:
        users = request.dbsession.query(User).all()
        schema = UserSchema(many=True)
        return {'status': 'success', 'data': schema.dump(users)}
    except Exception as e:
        log.error(f"Error fetching users: {str(e)}")
        return {'status': 'error', 'message': str(e)}