from abc import ABCMeta, abstractmethod
from werkzeug.datastructures import FileStorage

class Iimages(metaclass = ABCMeta):
    @abstractmethod
    def add(self, pic : FileStorage):
        pass

    @abstractmethod
    def edit(self, pic : FileStorage, path : str):
        pass

    @abstractmethod
    def get(self, file):
        pass

    @abstractmethod
    def remove(self, file_name):
        pass
