#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton.Singleton import Singleton
from src.DevelopToolBox.ContextManager.ABCAbstractCollection.ContextInterface import ContextInterface


class ContextManagerInterface(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self) -> ContextInterface:
        pass
