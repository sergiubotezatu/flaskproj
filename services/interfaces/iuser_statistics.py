from abc import ABCMeta, abstractmethod
from models.stats_model import StatisticsModel
from services.interfaces.iusers_repo import IUsersRepo


class IUserStatistics(metaclass = ABCMeta):
    @abstractmethod
    def get(self, id) -> StatisticsModel:
        pass