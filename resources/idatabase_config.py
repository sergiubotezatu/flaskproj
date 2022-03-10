from abc import ABCMeta, abstractmethod
from models.db_settings import DBSettings

class IDataBaseConfig(metaclass = ABCMeta):
    is_configured : bool

    @abstractmethod
    def add_settings(cls):
        pass

    @abstractmethod
    def load(self, settings : DBSettings):
        pass

    @abstractmethod
    def save(self):
        pass