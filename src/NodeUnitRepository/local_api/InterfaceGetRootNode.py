#
#
#
from abc import ABCMeta, abstractmethod
from Global2p1.NodeUnit import NodeUnit


class InterfaceGetRootNode(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_root_node(self, list_node: list[NodeUnit]) -> NodeUnit:
        pass
