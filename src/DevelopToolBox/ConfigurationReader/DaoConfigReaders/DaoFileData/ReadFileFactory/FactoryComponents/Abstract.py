#
#
#
from abc import ABCMeta, abstractmethod


class AbstractFactoryComponent():
    metaclass = ABCMeta

    @abstractmethod
    def read(self) -> dict:
        pass
