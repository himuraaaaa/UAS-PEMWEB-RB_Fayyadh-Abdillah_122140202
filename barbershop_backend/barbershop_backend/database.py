from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

Base = declarative_base()

class Database:
    def __init__(self, settings):
        self.engine = create_engine(settings['sqlalchemy.url'])
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        
    def initialize(self):
        Base.metadata.create_all(self.engine)
        
    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            
    def get_session(self):
        return self.Session() 