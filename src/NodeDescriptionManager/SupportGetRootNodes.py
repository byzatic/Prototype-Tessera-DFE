#
#
#
import logging
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.NodeUnit import NodeUnit


class SupportGetRootNodes(object):
    def __init__(self, graph_data_repository: InterfaceNodeUnitRepository):
        self.__logger: logging.Logger = logging.getLogger("GraphIterator-logger")
        self.__GraphDataRepository: InterfaceNodeUnitRepository = graph_data_repository

    def get_root_nodes(self):
        all_node_units: list[NodeUnit] = self.__GraphDataRepository.get_all_node_unit()
        list_all_root_nodes: list[NodeUnit] = []
        for node_unit in all_node_units:
            if node_unit.get_upstream() == []:
                list_all_root_nodes.append(node_unit)
        return list_all_root_nodes

