from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime as dtm
from app.model.Base import Base


class PriceQuote(Base):
    __tablename__ = 'price_quote'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(6), nullable=False)
    datetime = Column(DateTime, nullable=False)
    high = Column(Float(precision=32), nullable=False)
    low = Column(Float(precision=32), nullable=False)
    volume = Column(Integer(), nullable=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, symbol, dt, high, low, volume=None):
        self.symbol = symbol
        self.datetime = dt
        self.high = high
        self.low = low
        self.volume = volume
        self.created_at = dtm.now()

    def to_dict(self):
        return {
            'datetime': self.datetime,
            'high': self.high,
            'low': self.low
        }
