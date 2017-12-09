from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Connection:

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Connection.__instance is None:
            Connection()
        return Connection.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Connection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Connection.__instance = self
            self.__init_db()

    def __init_db(self):
        self.engine = create_engine('sqlite:///forex_analyzer.db', echo=True)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        print(database_exists(self.engine.url))

    def get_engine(self):
        return self.engine
