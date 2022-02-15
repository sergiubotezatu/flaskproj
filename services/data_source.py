from abc import ABCMeta, abstractmethod

class ISource(metaclass = ABCMeta):
    
    @abstractmethod
    def add_post(self, post):
        pass

    @abstractmethod
    def replace(self, post, post_id):
        pass

    @abstractmethod
    def remove(self, post_id):
        pass