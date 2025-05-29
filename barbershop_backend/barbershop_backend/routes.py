def includeme(config):
    print("ROUTES.PY includeme DIPANGGIL")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('assets', 'assets', cache_max_age=3600)
    
    # Auth routes
    config.add_route('api.auth.login', '/api/auth/login', request_method=('POST', 'OPTIONS'))
    config.add_route('api.auth.register', '/api/auth/register', request_method=('POST', 'OPTIONS'))
    config.add_route('api.auth.logout', '/api/auth/logout', request_method=('POST', 'OPTIONS'))
    
    # Upload route
    config.add_route('api.upload', '/api/upload', request_method=('POST', 'OPTIONS'))
    
    # Barber routes
    config.add_route('api.barbers', '/api/barbers', request_method=('GET', 'OPTIONS'))
    config.add_route('api.barber', '/api/barber/{id}', request_method=('GET', 'OPTIONS'))
    config.add_route('api.barber.create', '/api/barber/create', request_method=('POST', 'OPTIONS'))
    config.add_route('api.barber.update', '/api/barber/update/{id}', request_method=('PUT', 'OPTIONS'))
    config.add_route('api.barber.delete', '/api/barber/delete/{id}', request_method=('DELETE', 'OPTIONS'))
    
    # Service routes
    config.add_route('api.services', '/api/services', request_method=('GET', 'OPTIONS'))
    config.add_route('api.service', '/api/service/{id}', request_method=('GET', 'OPTIONS'))
    config.add_route('api.service.create', '/api/service/create', request_method=('POST', 'OPTIONS'))
    config.add_route('api.service.update', '/api/service/update/{id}', request_method=('PUT', 'OPTIONS'))
    config.add_route('api.service.delete', '/api/service/delete/{id}', request_method=('DELETE', 'OPTIONS'))
    
    # Appointment routes
    config.add_route('api.appointments', '/api/appointments', request_method=('GET', 'OPTIONS'))
    config.add_route('api.appointment', '/api/appointment/{id}', request_method=('GET', 'OPTIONS'))
    config.add_route('api.appointment.create', '/api/appointment/create', request_method=('POST', 'OPTIONS'))
    config.add_route('api.appointment.update', '/api/appointment/update/{id}', request_method=('PUT', 'OPTIONS'))
    config.add_route('api.appointment.delete', '/api/appointment/delete/{id}', request_method=('DELETE', 'OPTIONS'))
    config.add_route('api.appointment.update_status', '/api/appointment/update-status/{id}', request_method=('PUT', 'OPTIONS'))
    
    # User routes
    config.add_route('api.users', '/api/users', request_method=('GET', 'OPTIONS'))
    
    # Home route
    config.add_route('home', '/', request_method=('GET', 'OPTIONS'))