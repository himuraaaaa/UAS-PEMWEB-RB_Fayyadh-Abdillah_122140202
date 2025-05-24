from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class Appointment(BaseModel):
    """Appointment model for scheduling barber services"""
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    barber_id = Column(Integer, ForeignKey('barbers.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(20), default='pending')  # pending, confirmed, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="appointments")
    barber = relationship("Barber", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")

    def __init__(self, user_id, barber_id, service_id, appointment_date):
        self.user_id = user_id
        self.barber_id = barber_id
        self.service_id = service_id
        self.appointment_date = appointment_date

    def update_status(self, new_status):
        """Update appointment status"""
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False

    def to_dict(self):
        """Convert appointment instance to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'barber_id': self.barber_id,
            'service_id': self.service_id,
            'appointment_date': self.appointment_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 