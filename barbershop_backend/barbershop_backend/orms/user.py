from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, validates
from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel
import re

class User(BaseModel):
    """User ORM model with validation and database relationships"""
    __tablename__ = 'users'

    # username = Column(String(50), unique=True, nullable=True) # Make username nullable if not collected by form
    # Or consider removing username if not used
    username = Column(String(50), unique=True, nullable=True) # Temporarily make nullable
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=True) # Phone number might be optional

    # Database relationships
    appointments = relationship("Appointment", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, email, password, first_name, last_name, phone_number=None, username=None, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.username = username # Handle optional username
        self.set_password(password)
        self.is_admin = is_admin

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    @validates('username')
    def validate_username(self, key, username):
        """Validate username"""
        if username is not None and len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

    def set_password(self, password):
        """Hash and set password"""
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user instance to dictionary"""
        data = super().to_dict()
        # Remove sensitive data
        data.pop('password_hash', None)
        # Add related data
        data['appointments'] = [appointment.to_dict() for appointment in self.appointments]
        # Include new fields in to_dict
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['phone_number'] = self.phone_number
        return data

    @classmethod
    def get_by_email(cls, session, email):
        """Get user by email"""
        return session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_username(cls, session, username):
        """Get user by username"""
        return session.query(cls).filter(cls.username == username).first() 