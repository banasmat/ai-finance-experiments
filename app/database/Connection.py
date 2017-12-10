from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class Connection:

    __instance = None

    __engine_url = 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'storage', 'forex_analyzer.db')

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
        self.engine = create_engine(self.__engine_url, echo=True)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_engine_url(self):
        return self.__engine_url

    def get_engine(self):
        return self.engine

    def get_session(self):
        # self.engine.connect()
        return self.session
