from pyramid.httpexceptions import HTTPUnauthorized
import logging

log = logging.getLogger(__name__)

def auth_middleware(handler, registry):
    """
    Middleware untuk memverifikasi JWT token
    """
    def auth_tween(request):
        # Skip auth untuk endpoint yang tidak membutuhkan autentikasi (Guest access)
        # Endpoint GET untuk barbers (list dan detail)
        if request.method == 'GET' and request.path.startswith('/api/barbers'):
             log.info(f"Skipping authentication for GET {request.path}")
             return handler(request)

        # Endpoint GET untuk services (list dan detail)
        if request.method == 'GET' and request.path.startswith('/api/services'):
             log.info(f"Skipping authentication for GET {request.path}")
             return handler(request)

        # Skip auth untuk endpoint login dan register
        if request.path in ['/api/auth/login', '/api/auth/register']:
            log.info(f"Skipping authentication for {request.path}")
            return handler(request)

        # Cek header Authorization (untuk semua endpoint lain yang terproteksi)
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            log.warning(f"Authentication required for {request.path}: No Authorization header found")
            raise HTTPUnauthorized('Authentication required')

        # Verifikasi format token
        try:
            auth_type, token = auth_header.split(' ', 1)
            if auth_type.lower() != 'bearer':
                log.warning(f"Authentication failed for {request.path}: Invalid authentication type")
                raise HTTPUnauthorized('Invalid authentication type')
        except ValueError:
            log.warning(f"Authentication failed for {request.path}: Invalid Authorization header format")
            raise HTTPUnauthorized('Invalid authentication format')

        # Verifikasi token
        try:
            payload = request.jwt_manager.verify_token(token)
            # Tambahkan user info ke request
            request.user = payload
            log.info(f"Authenticated user: {payload['username']} for {request.path}")
        except Exception as e:
            log.error(f"Token verification failed for {request.path}: {str(e)}")
            raise HTTPUnauthorized('Invalid or expired token')

        return handler(request)

    return auth_tween

def includeme(config):
    """Pyramid configuration function"""
    config.add_tween('barbershop_backend.middleware.auth.auth_middleware') 