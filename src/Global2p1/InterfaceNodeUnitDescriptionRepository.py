#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.NodeUnit import NodeUnit


class InterfaceNodeUnitDescriptionRepository(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node_unit_description(self, node_unit_description: NodeUnit) -> NodeUnitDescription:
        pass

    @abstractmethod
    def get_all_node_unit_description(self) -> list[NodeUnitDescription]:
        pass

    @abstractmethod
    def get_root_node_unit_description(self) -> NodeUnitDescription:
        pass

    @abstractmethod
    def get_top_level_node_unit_descriptions(self) -> list[NodeUnitDescription]:
        pass
