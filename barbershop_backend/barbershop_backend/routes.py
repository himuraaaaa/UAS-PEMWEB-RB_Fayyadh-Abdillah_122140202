def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    # API Routes
    config.add_route('api.auth.login', '/api/auth/login', request_method='POST')
    config.add_route('api.auth.register', '/api/auth/register', request_method='POST')
    config.add_route('api.auth.logout', '/api/auth/logout', request_method='POST')
    
    # Barber Shop Routes
    config.add_route('api.barbers', '/api/barbers', request_method='GET')
    config.add_route('api.barber', '/api/barbers/{id}', request_method='GET')
    config.add_route('api.barber.create', '/api/barbers', request_method='POST')
    config.add_route('api.barber.update', '/api/barbers/{id}', request_method='PUT')
    config.add_route('api.barber.delete', '/api/barbers/{id}', request_method='DELETE')
    
    # Appointment Routes
    config.add_route('api.appointments', '/api/appointments', request_method='GET')
    config.add_route('api.appointment', '/api/appointments/{id}', request_method='GET')
    config.add_route('api.appointment.create', '/api/appointments', request_method='POST')
    config.add_route('api.appointment.update', '/api/appointments/{id}', request_method='PUT')
    config.add_route('api.appointment.delete', '/api/appointments/{id}', request_method='DELETE')
    
    # Service Routes
    config.add_route('api.services', '/api/services', request_method='GET')
    config.add_route('api.service', '/api/services/{id}', request_method='GET')
    config.add_route('api.service.create', '/api/services', request_method='POST')
    config.add_route('api.service.update', '/api/services/{id}', request_method='PUT')
    config.add_route('api.service.delete', '/api/services/{id}', request_method='DELETE')
