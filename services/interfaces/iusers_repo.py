from abc import ABCMeta, abstractmethod
from models.user import User

class IUsersRepo(metaclass = ABCMeta):
    
    @abstractmethod
    def add(self, user):
        pass

    @abstractmethod
    def get_by(self, **kwargs) -> User:
        pass

    @abstractmethod
    def remove(self, id):
        pass

    @abstractmethod
    def update(self, usr_id, user, pwd):
        pass

    @abstractmethod
    def has_account(self, user_id) -> bool:
        pass

        
