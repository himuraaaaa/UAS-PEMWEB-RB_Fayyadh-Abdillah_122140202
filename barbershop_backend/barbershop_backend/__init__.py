from pyramid.config import Configurator
from pyramid.view import view_config
from .database import Database
from .middleware.cors import add_cors_headers, cors_options_view
from .utils.jwt import includeme as jwt_includeme
from .middleware.auth import includeme as auth_includeme
import logging
import os

log = logging.getLogger(__name__)

# Test route untuk cek server
@view_config(route_name='test_route', renderer='json')
def test_view(request):
    return {'status': 'success', 'message': 'Test route works!'}

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    
    # Initialize database
    db = Database(settings)
    config.registry['db'] = db
    
    # Add request methods
    config.add_request_method(
        lambda request: request.registry['db'].get_session(),
        'dbsession',
        reify=True
    )
    
    # Configure JWT secret
    if 'jwt.secret' not in settings:
        settings['jwt.secret'] = os.environ.get('JWT_SECRET', 'your-secret-key')
        log.warning("Using default JWT secret key. Set JWT_SECRET environment variable for production.")
    
    # Add OPTIONS route for CORS preflight - harus di atas route lain
    config.add_route('cors_options', '/{path:.*}', request_method='OPTIONS')
    config.add_view(cors_options_view, route_name='cors_options')
    
    # Include routes
    config.include('.routes')
    
    # Add test route
    config.add_route('test_route', '/test')
    
    # Add CORS subscriber
    config.add_subscriber(add_cors_headers, 'pyramid.events.NewResponse')
    
    # Include JWT
    jwt_includeme(config)
    
    # Include Auth middleware
    auth_includeme(config)
    
    # Include Jinja2 renderer
    config.include('pyramid_jinja2')

    # Scan modul untuk view
    config.scan('.')
    
    # Print registered routes for debugging
    log.info("\n--- Registered Routes ---")
    for route in config.get_routes_mapper().get_routes():
        try:
            view_name = route.introspectable['callable'].__name__
        except (AttributeError, KeyError):
            view_name = "N/A or not directly callable"
        log.info(f"Name: {route.name}, Pattern: {route.pattern}, Methods: {route.methods}, View: {view_name}")
    log.info("-------------------------\n")

    return config.make_wsgi_app()