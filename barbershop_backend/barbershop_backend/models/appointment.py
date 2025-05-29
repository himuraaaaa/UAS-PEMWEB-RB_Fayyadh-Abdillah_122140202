from sqlalchemy import Column, Integer, ForeignKey, Date, Time, String, DateTime
from sqlalchemy.sql import func

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    barber_id = Column(Integer, ForeignKey('barbers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    notes = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default='pending')
    created_at = Column(DateTime, default=func.utcnow())
    updated_at = Column(DateTime, default=func.utcnow(), onupdate=func.utcnow()) 