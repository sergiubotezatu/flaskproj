from abc import ABCMeta, abstractmethod


class IDataBaseUpgrade:
   
    @abstractmethod
    def is_latest_version(self):
        pass

    abstractmethod
    def upgrade(self):
        pass