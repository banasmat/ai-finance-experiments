from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime as dtm
from app.model.Base import Base


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

    def __init__(self, currency, dt, title, actual=None, forecast=None, previous=None):
        self.currency = currency
        self.datetime = dt
        self.title = title
        self.actual = actual
        self.forecast = forecast
        self.previous = previous
        self.created_at = dtm.now()
