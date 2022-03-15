from abc import ABCMeta, abstractmethod
from services.database_config import DataBaseConfig

class IDataBase(metaclass = ABCMeta):
    config : DataBaseConfig

    @abstractmethod
    def initialize_db(cls):
        pass

    @abstractmethod
    def create_database(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def commit_and_close(self):
        pass