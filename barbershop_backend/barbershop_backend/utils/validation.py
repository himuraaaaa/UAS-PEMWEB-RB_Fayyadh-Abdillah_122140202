from marshmallow import ValidationError
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
import json
import logging

log = logging.getLogger(__name__)

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
        log.warning(f"Validation error: {err.messages}")
        raise HTTPBadRequest(json_body={
            'status': 'error',
            'message': 'Validation error',
            'errors': err.messages
        })

    except Exception as e:
        log.error(f"Error during request validation: {type(e).__name__} - {str(e)}")
        raise HTTPInternalServerError({
             'status': 'error',
             'message': 'Internal server error during validation'
        }) 