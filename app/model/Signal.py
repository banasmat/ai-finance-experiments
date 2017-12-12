from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime as dtm

Base = declarative_base()


class Signal(Base):

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    symbol = Column(String(6), nullable=False)
    calendar_entry_id = Column(Integer, ForeignKey('calendar_entry.id'))
    calendar_entry = relationship('CalendarEntry')
    created_at = Column(DateTime, nullable=False)

    def __init__(self, value, symbol, calendar_entry):
        self.value = value
        self.symbol = symbol
        self.calendar_entry = calendar_entry
        self.calendar_entry_id = calendar_entry.id
        self.created_at = dtm.now()
