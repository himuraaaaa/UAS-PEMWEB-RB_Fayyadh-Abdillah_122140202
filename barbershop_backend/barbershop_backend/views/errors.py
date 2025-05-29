from pyramid.view import exception_view_config
from pyramid.httpexceptions import HTTPUnauthorized, HTTPForbidden
from ..middleware.cors import add_cors_headers_to_response
import logging

log = logging.getLogger(__name__)

@exception_view_config(HTTPUnauthorized)
def unauthorized_view(exc, request):
    """Handle 401 Unauthorized errors with CORS headers"""
    try:
        log.info("Handling 401 Unauthorized error")
        response = add_cors_headers_to_response(exc)
        return response
    except Exception as e:
        log.error(f"Error handling 401: {str(e)}")
        return exc

@exception_view_config(HTTPForbidden)
def forbidden_view(exc, request):
    """Handle 403 Forbidden errors with CORS headers"""
    try:
        log.info("Handling 403 Forbidden error")
        response = add_cors_headers_to_response(exc)
        return response
    except Exception as e:
        log.error(f"Error handling 403: {str(e)}")
        return exc