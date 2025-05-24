from marshmallow import ValidationError
from pyramid.response import Response
import json

def validate_request(schema, request):
    """
    Validate request data against schema
    
    Args:
        schema: Marshmallow schema instance
        request: Pyramid request object
    
    Returns:
        tuple: (validated_data, error_response)
    """
    try:
        # Get request data
        if request.content_type == 'application/json':
            data = request.json_body
        else:
            data = request.POST

        # Validate data
        validated_data = schema.load(data)
        return validated_data, None

    except ValidationError as err:
        error_response = Response(
            json.dumps({
                'status': 'error',
                'message': 'Validation error',
                'errors': err.messages
            }),
            status=400,
            content_type='application/json'
        )
        return None, error_response

    except Exception as e:
        error_response = Response(
            json.dumps({
                'status': 'error',
                'message': str(e)
            }),
            status=500,
            content_type='application/json'
        )
        return None, error_response 