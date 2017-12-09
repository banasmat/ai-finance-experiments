from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime

Base = declarative_base()

class PriceRecord(Base):
    __tablename__ = 'price_record'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(6), nullable=False)
    datetime = Column(DateTime, nullable=False)
    high = Column(Float(precision=32), nullable=False)
    low = Column(Float(precision=32), nullable=False)
    created_at = Column(DateTime, nullable=False)
