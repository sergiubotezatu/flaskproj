from abc import ABCMeta, abstractmethod
from models.user import User

class IAuthentication(metaclass = ABCMeta):
    
    @abstractmethod
    def log_in_succesful(self, id, email, username) -> bool:
        pass

    @abstractmethod
    def log_out(self, id, email, username):
        pass

    @abstractmethod
    def is_any_logged_in(self) -> bool:
        pass

    @abstractmethod
    def is_logged_in(self, id) -> bool:
        pass

    @abstractmethod
    def get_logged_user(self) -> User:
        pass