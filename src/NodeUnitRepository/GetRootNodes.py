#
#
#
import logging
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.NodeUnit import NodeUnit
from LibByzaticCommon import Exceptions
from .GetTopLevelNodes import GetTopLevelNodes
from NodeUnitRepository.local_api.InterfaceGetTopLevelNodes import InterfaceGetTopLevelNodes
from .local_api.InterfaceGetRootNode import InterfaceGetRootNode

class GetRootNodes(InterfaceGetRootNode):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("NodeUnitRepository-logger")
        self.__SupportGetTopLevelNodes: InterfaceGetTopLevelNodes = GetTopLevelNodes()

    def get_root_node(self, list_node: list[NodeUnit]) -> NodeUnit:
        try:
            top_level_nodes: list[NodeUnit] = self.__SupportGetTopLevelNodes.get_top_level_nodes(list_node)
            if len(top_level_nodes) != 1:
                raise Exceptions.OperationIncompleteException(f"More then one root nodes found")
            else:
                return top_level_nodes[0]
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)
