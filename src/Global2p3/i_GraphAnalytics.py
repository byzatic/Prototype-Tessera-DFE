#
#
#
from abc import ABCMeta, abstractmethod
from LibByzaticCommon.Singleton import Singleton
from Global.NodeUnitDescription import NodeUnitDescription


class i_GraphAnalytics(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_path_from_source_node_to_root_node(self, source_node_description: NodeUnitDescription, root_node_description: NodeUnitDescription) -> list[NodeUnitDescription]:
        pass

    @abstractmethod
    def reverse_path(self, list_node_unit_descriptions: list[NodeUnitDescription]) -> list[NodeUnitDescription]:
        pass
