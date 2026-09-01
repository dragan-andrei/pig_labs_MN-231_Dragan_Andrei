from abc import ABC, abstractmethod

class Interface(ABC):
    @abstractmethod
    def set_parameter(self, params, value):
        pass

    @abstractmethod
    def get_parameter(self, params):
        pass