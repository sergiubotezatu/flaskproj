from abc import ABCMeta, abstractmethod
from models.logged_user import Logged_user

class ISessionMNGR(metaclass = ABCMeta):
    @abstractmethod
    def edit_logged(username, email):
        pass

    @abstractmethod
    def log_session(self, id, username, email, role):
        pass

    @abstractmethod
    def log_out(self):
        pass

    @abstractmethod
    def get_logged_user(self) -> Logged_user:
        pass