from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import validates
from datetime import datetime
import re

Base = declarative_base()

class BaseModel(Base):
    """Base class for all ORM models with validation and database features"""
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model instance to dictionary, handling datetime serialization"""
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # Format datetime objects to ISO 8601 string
            if isinstance(value, datetime):
                data[column.name] = value.isoformat()
            else:
                data[column.name] = value
        return data

    @classmethod
    def from_dict(cls, data):
        """Create model instance from dictionary with validation"""
        return cls(**{
            key: value for key, value in data.items()
            if key in cls.__table__.columns.keys()
        })

    @classmethod
    def get_by_id(cls, session, id):
        """Get model instance by ID"""
        return session.query(cls).filter(cls.id == id).first()

    @classmethod
    def get_all(cls, session):
        """Get all model instances"""
        return session.query(cls).all()

    def save(self, session):
        """Save model instance to database"""
        session.add(self)
        session.commit()
        return self

    def delete(self, session):
        """Delete model instance from database"""
        session.delete(self)
        session.commit()
        return True 