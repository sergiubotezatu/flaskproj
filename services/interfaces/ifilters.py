from abc import ABCMeta, abstractmethod
from collections import defaultdict

from services.interfaces.ipost_repo import IPostRepo

class IFilters(metaclass = ABCMeta):
    filtered_users : defaultdict
    unfiltered_users : set

    @abstractmethod
    def apply(self, query_params, page) -> list:
        pass

    @abstractmethod
    def get_new_querystr(self) -> str:
        pass
