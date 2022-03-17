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
    def get_user_by_mail(self, username):
        pass

    @abstractmethod
    def get_user_by_id(self, id):
        pass

    @abstractmethod
    def remove_user(self, user):
        pass

    @abstractmethod
    def update_user(self, user, pwd):
        pass
