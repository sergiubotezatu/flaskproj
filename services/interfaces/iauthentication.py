from abc import ABCMeta, abstractmethod
from models.logged_user import Logged_user

class IAuthentication(metaclass = ABCMeta):
    @abstractmethod
    def log_in(self, id, email, username) -> bool:
        pass

    @abstractmethod
    def log_out(self, id, email, username):
        pass

    @abstractmethod
    def is_logged_in(self, id) -> bool:
        pass

    @abstractmethod
    def get_logged_user(self) -> Logged_user:
        pass