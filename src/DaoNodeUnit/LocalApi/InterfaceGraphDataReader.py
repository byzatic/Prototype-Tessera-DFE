#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton


class InterfaceGraphDataReader(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_data(self, file_location: str) -> dict:
        pass
