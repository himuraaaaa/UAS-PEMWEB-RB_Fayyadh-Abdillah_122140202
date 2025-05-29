from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.tweens import EXCVIEW
import logging
import jwt

log = logging.getLogger(__name__)

def auth_tween(handler, registry):
    """Authentication tween that checks for valid JWT token"""
    def tween(request):
        # Skip authentication for OPTIONS requests
        if request.method == 'OPTIONS':
            log.info(f"Skipping authentication for OPTIONS {request.path}")
            return handler(request)
            
        # Skip authentication for static and assets
        if request.path.startswith('/assets/') or request.path.startswith('/static/'):
            log.info(f"Skipping authentication for static/assets {request.path}")
            return handler(request)
            
        # Skip authentication for login and register routes
        if request.path in ['/api/auth/login', '/api/auth/register']:
            log.info(f"Skipping authentication for {request.path}")
            return handler(request)
            
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            log.warning(f"Authentication required for {request.path}: No Authorization header found")
            response = HTTPUnauthorized('Authentication required')
            return response
            
        try:
            # Extract token from header
            auth_type, token = auth_header.split(' ', 1)
            if auth_type.lower() != 'bearer':
                log.warning(f"Invalid authentication type: {auth_type}")
                response = HTTPUnauthorized('Invalid authentication type')
                return response

            # Get JWT secret from settings
            jwt_secret = request.registry.settings.get('jwt.secret_key')
            if not jwt_secret:
                log.error("JWT secret not configured")
                response = HTTPUnauthorized('Server configuration error')
                return response

            # Verify token
            try:
                payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
                # Set both jwt and user attributes
                request.jwt = payload
                request.user = payload
                log.info(f"Authenticated user: {payload.get('username', 'unknown')} for {request.path}")
                log.debug(f"JWT payload: {payload}")
                return handler(request)
            except jwt.ExpiredSignatureError:
                log.warning(f"Token expired for {request.path}")
                response = HTTPUnauthorized('Token expired')
                return response
            except jwt.InvalidTokenError as e:
                log.warning(f"Invalid token for {request.path}: {str(e)}")
                response = HTTPUnauthorized('Invalid token')
                return response
                
        except Exception as e:
            log.error(f"Authentication failed for {request.path}: {str(e)}")
            response = HTTPUnauthorized('Authentication failed')
            return response
            
    return tween

def includeme(config):
    """Include the auth middleware"""
    config.add_tween('barbershop_backend.middleware.auth.auth_tween', under=EXCVIEW) 