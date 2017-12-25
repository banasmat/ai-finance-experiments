from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime as dtm
from app.model.Base import Base
from sqlalchemy.orm import relationship


class CalendarEntry(Base):
    __tablename__ = 'calendar_entry'

    id = Column(Integer, primary_key=True)
    currency = Column(String(3), nullable=False)
    datetime = Column(DateTime, nullable=False)
    title = Column(String(255), nullable=False)
    actual = Column(String(32), nullable=True)
    forecast = Column(String(32), nullable=True)
    previous = Column(String(32), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    signals = relationship("Signal", back_populates="calendar_entry")

    def __init__(self, currency, dt, title, actual=None, forecast=None, previous=None):
        self.currency = currency
        self.datetime = dt
        self.title = title
        self.actual = actual
        self.forecast = forecast
        self.previous = previous
        self.created_at = dtm.now()

    def to_dict(self):
        return {
            'symbol': self.currency,
            'title': self.title,
            'actual': self.actual,
            'forecast': self.forecast,
            'previous': self.previous,
            'datetime': self.datetime
        }
