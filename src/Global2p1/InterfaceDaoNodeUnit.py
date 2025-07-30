#
#
#
from abc import ABCMeta, abstractmethod
from Global2p1.NodeUnit import NodeUnit
from src.LibByzaticCommon.Singleton import Singleton


class InterfaceDaoNodeUnit(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node_unit(self, node_unit_id: str) -> NodeUnit:
        pass

    @abstractmethod
    def get_all_node_id(self) -> list[str]:
        pass
