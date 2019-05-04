from abc import ABCMeta, abstractmethod

class BasePreprocess:
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self._path = path


    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @abstractmethod
    def loadData(self):
        pass

