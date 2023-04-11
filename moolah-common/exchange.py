from abc import ABC, abstractmethod

# abstract class
class Exchange(ABC):

    def __init__(self):
        self._name = "Base"
        self._version = "0.01"

    @property
    def Name(self):
        return self._name

    @property
    def Version(self):
        return self._version

    @abstractmethod
    def execute(self, action, amount, coin):
        pass

    @abstractmethod
    def dump(self):
        pass

