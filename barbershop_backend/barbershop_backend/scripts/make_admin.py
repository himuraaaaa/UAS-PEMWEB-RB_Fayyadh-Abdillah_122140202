import argparse
import sys
from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import SQLAlchemyError
from ..orms import User

def make_admin(dbsession, email):
    """
    Make a user an admin by email
    """
    try:
        user = dbsession.query(User).filter_by(email=email).first()
        if not user:
            print(f"User with email {email} not found")
            return False
        
        user.is_admin = True
        dbsession.commit()
        print(f"Successfully made {email} an admin")
        return True
    except SQLAlchemyError as e:
        print(f"Database error: {str(e)}")
        dbsession.rollback()
        return False

def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('config_uri', help='Configuration file, e.g., development.ini')
    parser.add_argument('email', help='Email of the user to make admin')
    args = parser.parse_args(argv[1:])

    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            make_admin(dbsession, args.email)
    finally:
        env['closer']()

if __name__ == '__main__':
    main() 