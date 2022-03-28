from abc import ABCMeta, abstractmethod

class IPassHash(metaclass = ABCMeta):

    @staticmethod
    @abstractmethod
    def generate_pass(password):
        pass

    @staticmethod
    @abstractmethod
    def check_pass(password, input):
        pass