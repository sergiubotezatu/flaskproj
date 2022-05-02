from abc import ABCMeta, abstractmethod
from models.user import User
from services.interfaces.iauthentication import IAuthentication

class IAuthorization(metaclass = ABCMeta):
    
    @abstractmethod
    def is_owner(self, posts_instance, **kwargs):
        pass

    @abstractmethod
    def is_admin(self):
        pass

    @abstractmethod
    def is_owner_or_admin(self, posts_instance, **kwargs):
        pass

    @abstractmethod
    def is_default_admin(self, logged_user: User):
        pass

    @abstractmethod
    def is_member(self):
        pass