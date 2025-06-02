import pytest
from barbershop_backend.orms import Barber, Service, User
from pyramid.httpexceptions import HTTPForbidden

def test_create_barber(testapp, dbsession):
    # Create admin user first
    admin = User(
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    dbsession.add(admin)
    dbsession.flush()

    # Login as admin
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    token = login_response.json['token']

    # Create barber
    barber_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'bio': 'Experienced barber',
        'is_available': True
    }
    
    response = testapp.post_json('/api/barbers', 
                                barber_data,
                                headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.json['name'] == barber_data['name']
    assert response.json['email'] == barber_data['email']

def test_get_barbers(testapp, dbsession):
    # Create test barbers
    barber1 = Barber(
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        bio='Experienced barber',
        is_available=True
    )
    barber2 = Barber(
        name='Jane Smith',
        email='jane@example.com',
        phone='0987654321',
        bio='Master barber',
        is_available=True
    )
    dbsession.add_all([barber1, barber2])
    dbsession.flush()

    response = testapp.get('/api/barbers')
    assert response.status_code == 200
    assert len(response.json['data']) == 2

def test_create_service(testapp, dbsession):
    # Create admin user
    admin = User(
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    dbsession.add(admin)
    dbsession.flush()

    # Login as admin
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    token = login_response.json['token']

    # Create service
    service_data = {
        'name': 'Haircut',
        'description': 'Basic haircut service',
        'duration': 30,
        'price': 25.00
    }
    
    response = testapp.post_json('/api/services', 
                                service_data,
                                headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.json['name'] == service_data['name']
    assert response.json['price'] == service_data['price']

def test_get_services(testapp, dbsession):
    # Create test services
    service1 = Service(
        name='Haircut',
        description='Basic haircut service',
        duration=30,
        price=25.00
    )
    service2 = Service(
        name='Beard Trim',
        description='Beard trimming and shaping',
        duration=20,
        price=15.00
    )
    dbsession.add_all([service1, service2])
    dbsession.flush()

    response = testapp.get('/api/services')
    assert response.status_code == 200
    assert len(response.json['data']) == 2

def test_update_barber(testapp, dbsession):
    # Create admin user
    admin = User(
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    dbsession.add(admin)
    dbsession.flush()

    # Create barber
    barber = Barber(
        name='John Doe',
        email='john@example.com',
        phone='1234567890',
        bio='Experienced barber',
        is_available=True
    )
    dbsession.add(barber)
    dbsession.flush()

    # Login as admin
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    token = login_response.json['token']

    # Update barber
    update_data = {
        'name': 'John Updated',
        'bio': 'Updated bio'
    }
    
    response = testapp.put_json(f'/api/barbers/{barber.id}', 
                               update_data,
                               headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert response.json['name'] == update_data['name']
    assert response.json['bio'] == update_data['bio']

def test_delete_service(testapp, dbsession):
    # Create admin user
    admin = User(
        email='admin@example.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )
    dbsession.add(admin)
    dbsession.flush()

    # Create service
    service = Service(
        name='Test Service',
        description='Test description',
        duration=30,
        price=25.00
    )
    dbsession.add(service)
    dbsession.flush()

    # Login as admin
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    token = login_response.json['token']

    # Delete service
    response = testapp.delete(f'/api/services/{service.id}',
                            headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    
    # Verify service is deleted
    get_response = testapp.get(f'/api/services/{service.id}', status=404)
    assert get_response.status_code == 404 