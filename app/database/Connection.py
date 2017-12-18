import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class Connection:

    __instance = None

    __engine_url = "mysql://root:root@localhost/forex_analyzer_python"
    # __engine_url = 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'storage', 'forex_analyzer.db')

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

        config_path = os.path.join(os.path.abspath(os.getcwd()), 'config.yml')
        config = yaml.load(open(config_path))['database']

        self.__engine_url = config['engine'] + '://' + config['user'] + ':' + config['password'] + '@' + config['host'] + '/' + config['name']

        self.engine = create_engine(self.__engine_url, echo=False)

        Session = sessionmaker(bind=self.engine, autoflush=False)
        self.session = Session()

    def get_engine_url(self):
        return self.__engine_url

    def get_engine(self):
        return self.engine

    def get_session(self):
        # self.engine.connect()
        return self.session
