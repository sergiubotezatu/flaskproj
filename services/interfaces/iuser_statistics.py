from abc import ABCMeta, abstractmethod
from services.interfaces.iusers_repo import IUsersRepo


class IUserStatistics(metaclass = ABCMeta):
    @abstractmethod
    def get_table(self, user: IUsersRepo) -> bool:
        pass