from abc import ABCMeta, abstractmethod

class IUsers(metaclass = ABCMeta):
    
    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def check_pass(self):
        pass

    @abstractmethod
    def get_posts(self):
        pass

    @abstractmethod
    def get_user_by_name(self, username):
        pass
