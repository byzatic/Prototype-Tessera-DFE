#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton.Singleton import Singleton


class ApplicationStaticInterface(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, static_name: str) -> str:
        pass
