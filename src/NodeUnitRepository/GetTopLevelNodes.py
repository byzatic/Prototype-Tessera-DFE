#
#
#
import logging
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.NodeUnit import NodeUnit
from LibByzaticCommon import Exceptions
from .local_api.InterfaceGetTopLevelNodes import InterfaceGetTopLevelNodes


class GetTopLevelNodes(InterfaceGetTopLevelNodes):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("NodeUnitRepository-logger")

    def get_top_level_nodes(self, list_node_unit: list[NodeUnit]) -> list[NodeUnit]:
        try:
            all_node_units: list[NodeUnit] = list_node_unit
            list_all_root_nodes: list[NodeUnit] = []
            for node_unit in all_node_units:
                if node_unit.get_upstream() == []:
                    list_all_root_nodes.append(node_unit)
            return list_all_root_nodes
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)
