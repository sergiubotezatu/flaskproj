from abc import ABCMeta, abstractmethod
from services.database.database_config import DataBaseConfig

class IDataBase(metaclass = ABCMeta):
    config : DataBaseConfig

    @abstractmethod
    def upgrade_db(self):
        pass

    @abstractmethod
    def perform(self, query, *args, fetch = ""):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def commit_and_close(self):
        pass
    
    @classmethod
    @abstractmethod
    def set_db(cls):
        pass