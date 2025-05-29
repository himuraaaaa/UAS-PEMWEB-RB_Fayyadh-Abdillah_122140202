from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Barber(BaseModel):
    """Barber ORM model with validation and database relationships"""
    __tablename__ = 'barbers'

    name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    image = Column(String(255), nullable=False)
    social = Column(JSON, nullable=True)

    # Database relationships
    appointments = relationship("Appointment", back_populates="barber", cascade="all, delete-orphan")

    def __init__(self, name, position, image, social=None):
        self.name = name
        self.position = position
        self.image = image
        self.social = social

    def to_dict(self):
        """Convert barber instance to dictionary, avoiding recursion"""
        data = super().to_dict()
        data['appointment_ids'] = [appointment.id for appointment in self.appointments]
        return data

    @classmethod
    def get_available_barbers(cls, session):
        """Get all available barbers"""
        return session.query(cls).filter(cls.is_available == True).all()

    @classmethod
    def get_by_rating(cls, session, min_rating):
        """Get barbers with minimum rating"""
        return session.query(cls).filter(cls.rating >= min_rating).all() 