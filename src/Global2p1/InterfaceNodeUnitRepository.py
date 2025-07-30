#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.NodeUnit import NodeUnit


class InterfaceNodeUnitRepository(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node_unit(self, node_unit_description: NodeUnitDescription) -> NodeUnit:
        pass

    @abstractmethod
    def get_all_node_unit(self) -> list[NodeUnit]:
        pass

    @abstractmethod
    def get_root_node_unit(self) -> NodeUnit:
        pass

    @abstractmethod
    def get_top_level_node_units(self) -> list[NodeUnit]:
        pass
