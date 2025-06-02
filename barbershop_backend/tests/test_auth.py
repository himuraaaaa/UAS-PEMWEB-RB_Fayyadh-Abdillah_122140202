import pytest
from barbershop_backend.orms import User
from barbershop_backend.views.api import login
from pyramid.httpexceptions import HTTPForbidden

def test_user_login_success(testapp, dbsession):
    # Create test user
    user = User(
        email='test@example.com',
        password='testpassword123',
        first_name='Test',
        last_name='User',
        is_admin=True
    )
    dbsession.add(user)
    dbsession.flush()

    # Test login
    response = testapp.post_json('/api/auth/login', {
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    assert response.status_code == 200
    assert 'token' in response.json
    assert response.json['user']['email'] == 'test@example.com'
    assert response.json['user']['is_admin'] is True

def test_user_login_invalid_credentials(testapp):
    response = testapp.post_json('/api/auth/login', {
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    }, status=400)
    
    assert response.status_code == 400
    assert 'Invalid credentials' in response.json['message']

def test_user_login_missing_fields(testapp):
    response = testapp.post_json('/api/auth/login', {
        'email': 'test@example.com'
    }, status=400)
    
    assert response.status_code == 400
    assert 'password' in response.json['message']

def test_admin_access_control(testapp, dbsession):
    # Create regular user
    user = User(
        email='regular@example.com',
        password='testpassword123',
        first_name='Regular',
        last_name='User',
        is_admin=False
    )
    dbsession.add(user)
    dbsession.flush()

    # Login as regular user
    login_response = testapp.post_json('/api/auth/login', {
        'email': 'regular@example.com',
        'password': 'testpassword123'
    })
    
    token = login_response.json['token']
    
    # Try to access admin endpoint
    response = testapp.get('/api/users', 
                          headers={'Authorization': f'Bearer {token}'},
                          status=403)
    
    assert response.status_code == 403

def test_admin_access_success(testapp, dbsession):
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
    
    # Access admin endpoint
    response = testapp.get('/api/users', 
                          headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert 'data' in response.json

def test_password_hashing(dbsession):
    # Create user with password
    password = 'testpassword123'
    user = User(
        email='test@example.com',
        password=password,
        first_name='Test',
        last_name='User'
    )
    dbsession.add(user)
    dbsession.flush()

    # Verify password is hashed
    assert user.password != password
    assert user.check_password(password) is True
    assert user.check_password('wrongpassword') is False 