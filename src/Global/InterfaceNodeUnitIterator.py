#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository


class InterfaceNodeUnitIterator(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_next(self) -> NodeUnitDescription:
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass

    def reset(self) -> None:
        pass
