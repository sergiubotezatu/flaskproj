from werkzeug.datastructures import FileStorage
from abc import ABCMeta, abstractmethod
from models.post import Post

class IPostRepo(metaclass = ABCMeta):
    
    @abstractmethod
    def add(self, post : Post, img : FileStorage):
        pass

    @abstractmethod
    def replace(self, id, post : Post = None, img : FileStorage = None, img_src : str = ""):
        pass

    @abstractmethod
    def remove(self, post_id):
        pass

    @abstractmethod
    def get(self, post_id, email = None) -> Post:
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_image(self, post_id):
        pass

