from abc import ABCMeta, abstractmethod

from services.interfaces.ipost_repo import IPostRepo

class IFilters(metaclass = ABCMeta):
    @abstractmethod
    def set_not_filtered(self, posts : IPostRepo) -> set:
        pass
    
    @abstractmethod
    def set_current_filters(self):
        pass
        
    @abstractmethod
    def get_new_path(self) -> str:
        pass

    @abstractmethod
    def update_not_filtered(self, repo):
        pass

    @abstractmethod
    def set_not_filtered(self, repo):
        pass