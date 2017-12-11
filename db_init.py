from app.database.Connection import Connection
from sqlalchemy_utils import database_exists, create_database
from app.model.PriceQuote import PriceQuote
from app.model.CalendarEntry import CalendarEntry

engine_url = Connection.get_instance().get_engine_url()
engine = Connection.get_instance().get_engine()

if not database_exists(engine_url):
    create_database(engine_url)

    PriceQuote.metadata.create_all(engine)
    CalendarEntry.metadata.create_all(engine)

