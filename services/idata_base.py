from abc import ABCMeta, abstractmethod

class IDataBase(metaclass = ABCMeta):
    
    @abstractmethod
    def initialize_db(cls):
        pass

    @abstractmethod
    def create_database(self):
        pass