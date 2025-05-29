import jwt
from datetime import datetime, timedelta
from pyramid.settings import asbool
import logging
from functools import wraps
from pyramid.httpexceptions import HTTPUnauthorized

log = logging.getLogger(__name__)

class JWTManager:
    def __init__(self, secret_key, algorithm='HS256', expires_in=3600):
        """
        Initialize JWT manager
        
        Args:
            secret_key (str): Secret key for signing tokens
            algorithm (str): Algorithm to use for signing
            expires_in (int): Token expiration time in seconds
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in

    def create_token(self, user_id, username, is_admin=False):
        """
        Create a new JWT token
        
        Args:
            user_id (int): User ID
            username (str): Username
            is_admin (bool): Whether user is admin
            
        Returns:
            str: JWT token
        """
        try:
            payload = {
                'user_id': user_id,
                'username': username,
                'is_admin': is_admin,
                'exp': datetime.utcnow() + timedelta(seconds=self.expires_in),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            log.error(f"Error creating JWT token: {str(e)}")
            raise

    def verify_token(self, token):
        """
        Verify and decode a JWT token
        
        Args:
            token (str): JWT token to verify
            
        Returns:
            dict: Decoded token payload if valid
            
        Raises:
            jwt.InvalidTokenError: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            log.warning("JWT token has expired")
            raise
        except jwt.InvalidTokenError as e:
            log.error(f"Invalid JWT token: {str(e)}")
            raise

def require_jwt(view_func):
    """
    Decorator to require JWT authentication for a view
    
    Args:
        view_func: The view function to decorate
        
    Returns:
        function: Decorated view function
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Skip authentication for OPTIONS requests
        if request.method == 'OPTIONS':
            return view_func(request, *args, **kwargs)
            
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPUnauthorized('No valid authorization header')
            
        token = auth_header.split(' ')[1]
        try:
            payload = request.jwt_manager.verify_token(token)
            request.jwt = payload
            return view_func(request, *args, **kwargs)
        except jwt.InvalidTokenError as e:
            raise HTTPUnauthorized(str(e))
            
    return wrapped_view

def includeme(config):
    """Pyramid configuration function"""
    settings = config.get_settings()
    
    # Get JWT settings from config
    secret_key = settings.get('jwt.secret_key', 'your-secret-key-here')
    algorithm = settings.get('jwt.algorithm', 'HS256')
    expires_in = int(settings.get('jwt.expires_in', 3600))
    
    # Create JWT manager instance
    jwt_manager = JWTManager(secret_key, algorithm, expires_in)
    
    # Add JWT manager to registry
    config.registry.jwt_manager = jwt_manager
    
    # Add request method to get JWT manager
    def get_jwt_manager(request):
        return request.registry.jwt_manager
    
    config.add_request_method(get_jwt_manager, 'jwt_manager', reify=True) 