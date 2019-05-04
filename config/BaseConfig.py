from abc import ABCMeta, abstractmethod

class BaseConfig:
    __metaclass__ = ABCMeta

    def __init__(self, filename):
        self._profile = filename

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, filename):
        self._profile = filename

    @abstractmethod
    def parse(self):
        pass
