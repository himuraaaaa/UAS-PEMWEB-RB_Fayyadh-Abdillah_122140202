from pyramid.events import NewRequest
from pyramid.events import subscriber

@subscriber(NewRequest)
def add_cors_headers(event):
    """Add CORS headers to response"""
    request = event.request
    response = request.response

    # Allow requests from any origin
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    # Allow specific headers
    response.headers['Access-Control-Allow-Headers'] = (
        'Origin, Content-Type, Accept, Authorization, X-Request-With'
    )
    
    # Allow specific methods
    response.headers['Access-Control-Allow-Methods'] = (
        'GET, POST, PUT, DELETE, OPTIONS'
    )
    
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response.status = 200
        return response 