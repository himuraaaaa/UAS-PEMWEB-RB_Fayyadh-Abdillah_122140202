import pytest
from datetime import datetime, timedelta
from barbershop_backend.orms import User, Barber, Service, Appointment

def test_create_appointment(testapp, dbsession):
    # Create test user
    user = User(
        email='user@example.com',
        password='userpass123',
        first_name='Test',
        last_name='User'
    )
    dbsession.add(user)
    
    # Create test barber
    barber = Barber(
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        bio='Experienced barber',
        is_available=True
    )
    dbsession.add(barber)
    
    # Create test service
    service = Service(
        name='Haircut',
        description='Basic haircut service',
        duration=30,
        price=25.00
    )
    dbsession.add(service)
    dbsession.flush()

    # Login as user
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'user@example.com',
        'password': 'userpass123'
    })
    token = login_response.json['token']

    # Create appointment
    appointment_time = datetime.now() + timedelta(days=1)
    appointment_data = {
        'barber_id': barber.id,
        'service_id': service.id,
        'appointment_time': appointment_time.isoformat(),
        'notes': 'Test appointment'
    }
    
    response = testapp.post_json('/api/appointments', 
                                appointment_data,
                                headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.json['barber_id'] == barber.id
    assert response.json['service_id'] == service.id

def test_get_user_appointments(testapp, dbsession):
    # Create test user
    user = User(
        email='user@example.com',
        password='userpass123',
        first_name='Test',
        last_name='User'
    )
    dbsession.add(user)
    
    # Create test barber
    barber = Barber(
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        bio='Experienced barber',
        is_available=True
    )
    dbsession.add(barber)
    
    # Create test service
    service = Service(
        name='Haircut',
        description='Basic haircut service',
        duration=30,
        price=25.00
    )
    dbsession.add(service)
    dbsession.flush()

    # Create test appointments
    appointment1 = Appointment(
        user_id=user.id,
        barber_id=barber.id,
        service_id=service.id,
        appointment_time=datetime.now() + timedelta(days=1),
        status='scheduled'
    )
    appointment2 = Appointment(
        user_id=user.id,
        barber_id=barber.id,
        service_id=service.id,
        appointment_time=datetime.now() + timedelta(days=2),
        status='scheduled'
    )
    dbsession.add_all([appointment1, appointment2])
    dbsession.flush()

    # Login as user
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'user@example.com',
        'password': 'userpass123'
    })
    token = login_response.json['token']

    # Get user appointments
    response = testapp.get('/api/appointments',
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert len(response.json['data']) == 2

def test_cancel_appointment(testapp, dbsession):
    # Create test user
    user = User(
        email='user@example.com',
        password='userpass123',
        first_name='Test',
        last_name='User'
    )
    dbsession.add(user)
    
    # Create test barber
    barber = Barber(
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        bio='Experienced barber',
        is_available=True
    )
    dbsession.add(barber)
    
    # Create test service
    service = Service(
        name='Haircut',
        description='Basic haircut service',
        duration=30,
        price=25.00
    )
    dbsession.add(service)
    dbsession.flush()

    # Create test appointment
    appointment = Appointment(
        user_id=user.id,
        barber_id=barber.id,
        service_id=service.id,
        appointment_time=datetime.now() + timedelta(days=1),
        status='scheduled'
    )
    dbsession.add(appointment)
    dbsession.flush()

    # Login as user
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'user@example.com',
        'password': 'userpass123'
    })
    token = login_response.json['token']

    # Cancel appointment
    response = testapp.put_json(f'/api/appointments/{appointment.id}/cancel',
                              {},
                              headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.json['status'] == 'cancelled'

def test_get_barber_appointments(testapp, dbsession):
    # Create test barber
    barber = Barber(
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        bio='Experienced barber',
        is_available=True
    )
    dbsession.add(barber)
    
    # Create test service
    service = Service(
        name='Haircut',
        description='Basic haircut service',
        duration=30,
        price=25.00
    )
    dbsession.add(service)
    
    # Create test users
    user1 = User(
        email='user1@example.com',
        password='userpass123',
        first_name='User',
        last_name='One'
    )
    user2 = User(
        email='user2@example.com',
        password='userpass123',
        first_name='User',
        last_name='Two'
    )
    dbsession.add_all([user1, user2])
    dbsession.flush()

    # Create test appointments
    appointment1 = Appointment(
        user_id=user1.id,
        barber_id=barber.id,
        service_id=service.id,
        appointment_time=datetime.now() + timedelta(days=1),
        status='scheduled'
    )
    appointment2 = Appointment(
        user_id=user2.id,
        barber_id=barber.id,
        service_id=service.id,
        appointment_time=datetime.now() + timedelta(days=2),
        status='scheduled'
    )
    dbsession.add_all([appointment1, appointment2])
    dbsession.flush()

    # Login as admin
    admin = User(
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    dbsession.add(admin)
    dbsession.flush()

    login_response = testapp.post_json('/api/auth/login', {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    token = login_response.json['token']

    # Get barber appointments
    response = testapp.get(f'/api/barbers/{barber.id}/appointments',
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert len(response.json['data']) == 2

def test_appointment_validation(testapp, dbsession):
    # Create test user
    user = User(
        email='user@example.com',
        password='userpass123',
        first_name='Test',
        last_name='User'
    )
    dbsession.add(user)
    
    # Create test barber
    barber = Barber(
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        bio='Experienced barber',
        is_available=True
    )
    dbsession.add(barber)
    
    # Create test service
    service = Service(
        name='Haircut',
        description='Basic haircut service',
        duration=30,
        price=25.00
    )
    dbsession.add(service)
    dbsession.flush()

    # Login as user
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'user@example.com',
        'password': 'userpass123'
    })
    token = login_response.json['token']

    # Try to create appointment in the past
    past_time = datetime.now() - timedelta(days=1)
    appointment_data = {
        'barber_id': barber.id,
        'service_id': service.id,
        'appointment_time': past_time.isoformat(),
        'notes': 'Test appointment'
    }
    
    response = testapp.post_json('/api/appointments', 
                                appointment_data,
                                headers={'Authorization': f'Bearer {token}'},
                                status=400)
    
    assert response.status_code == 400
    assert 'past' in response.json['message'].lower() 