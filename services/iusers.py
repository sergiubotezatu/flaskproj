from abc import ABCMeta, abstractmethod

class IUsers(metaclass = ABCMeta):
    
    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def get_posts(self, user_id):
        pass

    @abstractmethod
    def get_user_by_mail(self, mail):
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

    @abstractmethod
    def has_account(self, user_id) -> bool:
        pass
