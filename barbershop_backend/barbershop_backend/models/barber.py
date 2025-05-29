from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func

class Barber(Base):
    __tablename__ = 'barbers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    image = Column(String(255), nullable=False)
    social = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.utcnow())
    updated_at = Column(DateTime, default=func.utcnow(), onupdate=func.utcnow()) 