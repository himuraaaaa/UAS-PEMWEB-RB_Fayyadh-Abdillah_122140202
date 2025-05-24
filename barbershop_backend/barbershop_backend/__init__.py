from pyramid.config import Configurator
from .database import Database
from .middleware.cors import add_cors_headers
from .utils.jwt import includeme as jwt_includeme
from .middleware.auth import includeme as auth_includeme


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
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
    
    # Include routes
    config.include('.routes')
    
    # Add CORS subscriber
    config.add_subscriber(add_cors_headers, 'pyramid.events.NewRequest')
    
    # Include JWT
    jwt_includeme(config)
    
    # Include Auth middleware
    auth_includeme(config)
    
    # Include Jinja2 renderer
    config.include('pyramid_jinja2')
    
    # Scan for views
    config.scan()
    
    return config.make_wsgi_app()
