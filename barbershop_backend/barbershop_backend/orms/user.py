from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship, validates
from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel
import re

class User(BaseModel):
    """User ORM model with validation and database relationships"""
    __tablename__ = 'users'

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    # Database relationships
    appointments = relationship("Appointment", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
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
        if len(username) < 3:
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
        return data

    @classmethod
    def get_by_email(cls, session, email):
        """Get user by email"""
        return session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_username(cls, session, username):
        """Get user by username"""
        return session.query(cls).filter(cls.username == username).first() 