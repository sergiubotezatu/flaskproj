from abc import ABCMeta, abstractmethod
from collections import defaultdict

from services.interfaces.ipost_repo import IPostRepo

class IFilters(metaclass = ABCMeta):
    applied : defaultdict
    available : set
    filtered_ids : list
    filtered_names : list
    
    @abstractmethod
    def apply(self, query_params, page) -> list:
        pass

    @abstractmethod
    def set_newly_applied(self, query_params):
        pass
        
    @abstractmethod
    def get_new_querystr(self) -> str:
        pass

    @abstractmethod
    def update_available(self):
        pass

    @abstractmethod
    def reset_available(self):
        pass