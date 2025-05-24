from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import relationship, validates
from .base import BaseModel
import re

class Barber(BaseModel):
    """Barber ORM model with validation and database relationships"""
    __tablename__ = 'barbers'

    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20))
    bio = Column(String(500))
    rating = Column(Float, default=0.0)
    is_available = Column(Boolean, default=True)

    # Database relationships
    appointments = relationship("Appointment", back_populates="barber", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="barber", cascade="all, delete-orphan")

    def __init__(self, name, email, phone=None, bio=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.bio = bio

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        """Validate phone number format"""
        if phone and not re.match(r"^\+?1?\d{9,15}$", phone):
            raise ValueError("Invalid phone number format")
        return phone

    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate rating value"""
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        return rating

    def update_rating(self, new_rating):
        """Update barber's rating with validation"""
        if new_rating < 0 or new_rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        if self.rating == 0:
            self.rating = new_rating
        else:
            self.rating = (self.rating + new_rating) / 2

    def to_dict(self):
        """Convert barber instance to dictionary, avoiding recursion"""
        data = super().to_dict()
        # Add related data (avoiding full recursion)
        # Hanya sertakan daftar ID service, bukan objek service lengkap yang bisa memicu rekursi kembali ke barber
        data['service_ids'] = [service.id for service in self.services]
        # Untuk appointment, bisa sertakan data dasar atau ID
        # Contoh: sertakan hanya ID appointment
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