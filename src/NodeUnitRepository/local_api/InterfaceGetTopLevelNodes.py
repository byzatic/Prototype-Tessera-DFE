#
#
#
from abc import ABCMeta, abstractmethod
from Global2p1.NodeUnit import NodeUnit


class InterfaceGetTopLevelNodes(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_top_level_nodes(self, list_node_unit: list[NodeUnit]) -> list[NodeUnit]:
        pass
