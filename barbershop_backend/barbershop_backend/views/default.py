from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError

from ..orms import User, Barber, Service, Appointment

@view_config(route_name='home', renderer='json')
def home_view(request):
    """Home view that returns basic API information"""
    return {
        'status': 'success',
        'message': 'Welcome to Barbershop API',
        'endpoints': {
            'auth': {
                'login': '/api/auth/login',
                'register': '/api/auth/register'
            },
            'barbers': {
                'list': '/api/barbers',
                'detail': '/api/barber/{id}',
                'create': '/api/barber/create'
            },
            'services': {
                'list': '/api/services'
            },
            'appointments': {
                'list': '/api/appointments',
                'create': '/api/appointment/create'
            }
        }
    }

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
