#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton.Singleton import Singleton


class ContextInterface(Singleton):
    metaclass = ABCMeta

    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def get_all(self) -> dict:
        pass

    @abstractmethod
    def contains(self, key: str) -> bool:
        pass
