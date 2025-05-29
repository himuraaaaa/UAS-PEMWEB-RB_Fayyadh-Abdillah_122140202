from pyramid.events import NewResponse
from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPOk
import logging

log = logging.getLogger(__name__)

def add_cors_headers_to_response(response):
    """Helper function to add CORS headers to any response"""
    try:
        # Allow both localhost and 127.0.0.1
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = (
            'Origin, Content-Type, Accept, Authorization, X-Requested-With'
        )
        response.headers['Access-Control-Allow-Methods'] = (
            'GET, POST, PUT, DELETE, OPTIONS'
        )
        response.headers['Access-Control-Max-Age'] = '3600'  # 1 hour
        return response
    except Exception as e:
        log.error(f"Error adding CORS headers: {str(e)}")
        return response

@subscriber(NewResponse)
def add_cors_headers(event):
    """Add CORS headers to all responses"""
    try:
        response = event.response
        add_cors_headers_to_response(response)
    except Exception as e:
        log.error(f"Error in CORS subscriber: {str(e)}")

def cors_options_view(request):
    """Handle OPTIONS requests for CORS preflight"""
    try:
        log.info(f"Handling OPTIONS request for {request.path}")
        response = HTTPOk()
        response = add_cors_headers_to_response(response)
        return response
    except Exception as e:
        log.error(f"Error handling OPTIONS request: {str(e)}")
        response = HTTPOk()
        return response 