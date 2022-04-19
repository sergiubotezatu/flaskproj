from abc import ABCMeta, abstractmethod
from models.post import Post

class IPostRepo(metaclass = ABCMeta):
    
    @abstractmethod
    def add(self, post):
        pass

    @abstractmethod
    def replace(self, post, post_id):
        pass

    @abstractmethod
    def remove(self, post_id):
        pass

    @abstractmethod
    def get(self, post_id) -> Post:
        pass

    @abstractmethod
    def get_all(self):
        pass
