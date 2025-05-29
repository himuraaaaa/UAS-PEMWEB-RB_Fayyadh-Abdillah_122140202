from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Service(BaseModel):
    """Service model for barber shop services"""
    __tablename__ = 'services'

    name = Column(String(100), nullable=False)
    description = Column(String(500))
    duration = Column(Integer)  # Duration in minutes
    price = Column(Float, nullable=False)
    image = Column(String(255), nullable=False)

    # Relationships
    appointments = relationship("Appointment", back_populates="service")

    def __init__(self, name, price, image, description=None, duration=None):
        self.name = name
        self.price = price
        self.image = image
        self.description = description
        self.duration = duration

    def to_dict(self):
        """Convert service instance to dictionary, avoiding recursion"""
        data = super().to_dict()
        return data

    @classmethod
    def get_available_barbers(cls, session):
        """Get all available barbers"""
        return session.query(cls).filter(cls.is_available == True).all()

    @classmethod
    def get_by_rating(cls, session, min_rating):
        """Get barbers with minimum rating"""
        return session.query(cls).filter(cls.rating >= min_rating).all() 