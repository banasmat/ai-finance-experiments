from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime as dtm

Base = declarative_base()


class CalendarEntry(Base):
    __tablename__ = 'calendar_entry'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(6), nullable=False)
    datetime = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    actual = Column(String, nullable=True)
    forecast = Column(String, nullable=True)
    previous = Column(String, nullable=True)
    signal = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, symbol, dt, title, actual=None, forecast=None, previous=None):
        self.symbol = symbol
        self.datetime = dt
        self.title = title
        self.actual = actual
        self.forecast = forecast
        self.previous = previous
        self.created_at = dtm.now()
