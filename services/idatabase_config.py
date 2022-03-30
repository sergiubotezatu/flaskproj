from abc import ABCMeta, abstractmethod
from models.db_settings import DBSettings

class IDataBaseConfig(metaclass = ABCMeta):
    
    @classmethod
    @abstractmethod
    def is_configured(cls) -> bool:
        pass

    @abstractmethod
    def add_settings(cls):
        pass

    @abstractmethod
    def load(self, settings : DBSettings):
        pass

    @abstractmethod
    def save(self):
        pass