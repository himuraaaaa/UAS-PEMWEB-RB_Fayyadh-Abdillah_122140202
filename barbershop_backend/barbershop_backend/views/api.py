from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest, HTTPForbidden
from sqlalchemy.exc import SQLAlchemyError
from ..orms import User, Barber, Service, Appointment
from ..schemas.user_schema import UserSchema, UserLoginSchema
from ..schemas.barber_schema import BarberSchema, BarberUpdateSchema
from ..schemas.service_schema import ServiceUpdateSchema
from ..utils.validation import validate_request
from datetime import datetime
import json
import logging

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

@view_config(route_name='api.auth.register', renderer='json', request_method='POST')
def register(request):
    # Validate request data
    schema = UserSchema()
    data, error = validate_request(schema, request)
    if error:
        return error

    try:
        log.info(f"Attempting to register user with email: {data['email']}")
        
        # Check if user already exists
        existing_user = request.dbsession.query(User).filter_by(email=data['email']).first()
        if existing_user:
            log.warning(f"Registration failed: Email {data['email']} already registered")
            return {'status': 'error', 'message': 'Email already registered'}

        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']  # Password will be hashed in __init__
        )
        request.dbsession.add(user)
        
        # Commit the transaction to ensure data is saved
        request.dbsession.commit()
        
        log.info(f"Successfully registered user: {user.username} with ID: {user.id}")
        return {'status': 'success', 'user_id': user.id}
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

# Barber Views
@view_config(route_name='api.barbers', renderer='json', request_method='GET')
def get_barbers(request):
    try:
        barbers = request.dbsession.query(Barber).all()
        schema = BarberSchema(many=True)
        return {'status': 'success', 'data': schema.dump(barbers)}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.barber', renderer='json', request_method='GET')
def get_barber(request):
    try:
        barber_id = request.matchdict['id']
        barber = request.dbsession.query(Barber).get(barber_id)
        if not barber:
            return HTTPNotFound()
        return {'status': 'success', 'data': barber.to_dict()}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.barber.create', renderer='json', request_method='POST')
def create_barber(request):
    # Periksa apakah user adalah admin
    if not request.user.get('is_admin', False):
        log.warning(f"Unauthorized attempt to create barber by user: {request.user.get('username', 'Unknown')}")
        raise HTTPForbidden('Admin access required')

    # Validate request data
    schema = BarberSchema()
    data, error = validate_request(schema, request)
    if error:
        return error

    try:
        log.info(f"Attempting to create barber with name: {data['name']}")
        barber = Barber(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            bio=data.get('bio')
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
    # Periksa apakah user adalah admin
    if not request.user.get('is_admin', False):
        log.warning(f"Unauthorized attempt to update barber by user: {request.user.get('username', 'Unknown')}")
        raise HTTPForbidden('Admin access required')

    barber_id = request.matchdict.get('id')
    if not barber_id:
        raise HTTPBadRequest('Barber ID is required')

    try:
        barber = request.dbsession.query(Barber).get(barber_id)
        if not barber:
            raise HTTPNotFound('Barber not found')

        # Validate request data using update schema
        schema = BarberUpdateSchema()
        data, error = validate_request(schema, request)
        if error:
            return error

        # Update barber object with validated data
        for key, value in data.items():
            setattr(barber, key, value)

        request.dbsession.commit()
        log.info(f"Successfully updated barber with ID: {barber_id} by admin: {request.user.get('username', 'Unknown')}")
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
    # Periksa apakah user adalah admin
    if not request.user.get('is_admin', False):
        log.warning(f"Unauthorized attempt to delete barber by user: {request.user.get('username', 'Unknown')}")
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
        log.info(f"Successfully deleted barber with ID: {barber_id} by admin: {request.user.get('username', 'Unknown')}")
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
        return {'status': 'success', 'data': [service.to_dict() for service in services]}
    except Exception as e:
        log.error(f"Error fetching services: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.service', renderer='json', request_method='GET')
def get_service(request):
    """Get a single service by ID"""
    try:
        service_id = request.matchdict.get('id')
        if not service_id:
             raise HTTPBadRequest('Service ID is required')

        service = request.dbsession.query(Service).get(service_id)

        if not service:
            log.warning(f"Service with ID {service_id} not found")
            raise HTTPNotFound('Service not found')

        log.info(f"Successfully fetched service with ID: {service_id}")
        return {'status': 'success', 'data': service.to_dict()}

    except HTTPNotFound:
        request.dbsession.rollback()
        raise
    except HTTPBadRequest:
        request.dbsession.rollback()
        raise
    except Exception as e:
        log.error(f"Error fetching service {service_id}: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': 'An error occurred while fetching the service'}

@view_config(route_name='api.service.create', renderer='json', request_method='POST')
def create_service(request):
    # Periksa apakah user adalah admin
    if not request.user.get('is_admin', False):
        log.warning(f"Unauthorized attempt to create service by user: {request.user.get('username', 'Unknown')}")
        raise HTTPForbidden('Admin access required')

    # Anda mungkin perlu membuat ServiceSchema untuk validasi input
    # Sementara ini, kita akan langsung menggunakan request.json_body
    try:
        data = request.json_body
        log.info(f"Attempting to create service with name: {data.get('name')}")
        service = Service(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            barber_id=data.get('barber_id') # Ambil barber_id dari data
        )
        request.dbsession.add(service)
        request.dbsession.commit()
        log.info(f"Successfully created service with ID: {service.id}")
        return {'status': 'success', 'service_id': service.id}
    except Exception as e:
        log.error(f"Error creating service: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.service.update', renderer='json', request_method='PUT')
def update_service(request):
    # Periksa apakah user adalah admin
    if not request.user.get('is_admin', False):
        log.warning(f"Unauthorized attempt to update service by user: {request.user.get('username', 'Unknown')}")
        raise HTTPForbidden('Admin access required')

    service_id = request.matchdict.get('id')
    if not service_id:
        raise HTTPBadRequest('Service ID is required')

    try:
        service = request.dbsession.query(Service).get(service_id)
        if not service:
            raise HTTPNotFound('Service not found')

        # Validate request data using update schema
        schema = ServiceUpdateSchema()
        data, error = validate_request(schema, request)
        if error:
            return error

        # Update service object with validated data
        for key, value in data.items():
            # Pastikan hanya field yang diizinkan dalam schema update yang diupdate
            if hasattr(service, key):
                 setattr(service, key, value)

        request.dbsession.commit()
        log.info(f"Successfully updated service with ID: {service_id} by admin: {request.user.get('username', 'Unknown')}")
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
    # Periksa apakah user adalah admin
    if not request.user.get('is_admin', False):
        log.warning(f"Unauthorized attempt to delete service by user: {request.user.get('username', 'Unknown')}")
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
        log.info(f"Successfully deleted service with ID: {service_id} by admin: {request.user.get('username', 'Unknown')}")
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
        # Cek apakah user adalah admin
        if not request.user.get('is_admin', False):
            # Jika bukan admin, hanya tampilkan appointment user tersebut
            appointments = request.dbsession.query(Appointment).filter_by(user_id=request.user['user_id']).all()
        else:
            # Jika admin, tampilkan semua appointment
            appointments = request.dbsession.query(Appointment).all()
            
        return {'status': 'success', 'data': [appointment.to_dict() for appointment in appointments]}
    except Exception as e:
        log.error(f"Error getting appointments: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.appointment.create', renderer='json', request_method='POST')
def create_appointment(request):
    try:
        data = request.json_body
        log.info(f"Received data for appointment creation: {data}")
        # Gunakan user_id dari token
        appointment = Appointment(
            user_id=request.user['user_id'],  # Gunakan ID dari token
            barber_id=data['barber_id'],
            service_id=data['service_id'],
            appointment_date=datetime.fromisoformat(data['appointment_date']),
        )
        request.dbsession.add(appointment)
        request.dbsession.commit()
        log.info(f"Successfully created appointment with ID: {appointment.id}")
        return {'status': 'success', 'appointment_id': appointment.id}
    except Exception as e:
        log.error(f"Error creating appointment: {str(e)}")
        request.dbsession.rollback()
        return {'status': 'error', 'message': str(e)}

@view_config(route_name='api.appointment.update', renderer='json', request_method='PUT')
def update_appointment(request):
    """Update a specific appointment by ID"""
    appointment_id = request.matchdict.get('id')
    if not appointment_id:
        raise HTTPBadRequest('Appointment ID is required')

    try:
        appointment = request.dbsession.query(Appointment).get(appointment_id)
        if not appointment:
            raise HTTPNotFound('Appointment not found')

        # Otorisasi: Hanya admin atau pemilik appointment yang bisa mengupdate
        if not request.user.get('is_admin', False) and appointment.user_id != request.user.get('user_id'):
             log.warning(f"Unauthorized attempt to update appointment {appointment_id} by user: {request.user.get('username', 'Unknown')}")
             raise HTTPForbidden('You can only update your own appointments')

        # TODO: Tambahkan validasi input menggunakan schema jika diperlukan
        data = request.json_body

        # Update appointment fields (hanya field yang diizinkan diupdate oleh user)
        # Admin bisa mengupdate semua field, user biasa mungkin terbatas
        # Untuk saat ini, kita biarkan admin dan user biasa bisa mengupdate beberapa field yang sama
        allowed_fields = ['barber_id', 'service_id', 'appointment_date'] # Contoh field yang diizinkan
        for field, value in data.items():
             if field in allowed_fields:
                  if field == 'appointment_date':
                       # Konversi string ISO 8601 ke datetime object
                       setattr(appointment, field, datetime.fromisoformat(value))
                  else:
                       setattr(appointment, field, value)
             # Jika admin, bisa update field lain jika ada (misal: status)
             elif request.user.get('is_admin', False) and hasattr(appointment, field):
                  setattr(appointment, field, value)

        request.dbsession.commit()
        log.info(f"Successfully updated appointment with ID: {appointment_id} by user: {request.user.get('username', 'Unknown')}")
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
    """Delete a specific appointment by ID"""
    appointment_id = request.matchdict.get('id')
    if not appointment_id:
        raise HTTPBadRequest('Appointment ID is required')

    try:
        appointment = request.dbsession.query(Appointment).get(appointment_id)
        if not appointment:
            raise HTTPNotFound('Appointment not found')

        # Otorisasi: Hanya admin atau pemilik appointment yang bisa menghapus
        if not request.user.get('is_admin', False) and appointment.user_id != request.user.get('user_id'):
             log.warning(f"Unauthorized attempt to delete appointment {appointment_id} by user: {request.user.get('username', 'Unknown')}")
             raise HTTPForbidden('You can only delete your own appointments')

        request.dbsession.delete(appointment)
        request.dbsession.commit()
        log.info(f"Successfully deleted appointment with ID: {appointment_id} by user: {request.user.get('username', 'Unknown')}")
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