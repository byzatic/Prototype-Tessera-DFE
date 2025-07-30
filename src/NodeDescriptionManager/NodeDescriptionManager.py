#
#
#
import logging
from Global2p1.NodeUnit import NodeUnit
from Global2p2.InterfaceNodeDescriptionManager import InterfaceNodeDescriptionManager
from Global.NodeUnitDescription import NodeUnitDescription
from .SupportGetRootNodes import SupportGetRootNodes
from .SupportConvertDtoToEntity import SupportConvertDtoToEntity
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from src.LibByzaticCommon import Exceptions


class NodeDescriptionManager(InterfaceNodeDescriptionManager):
    def __init__(self, graph_data_repository: InterfaceNodeUnitRepository):
        self.__logger: logging.Logger = logging.getLogger("NodeDescriptionManager-logger")
        self.__SupportGetRootNodes: SupportGetRootNodes = SupportGetRootNodes(graph_data_repository)
        self.__SupportConvertDtoToEntity: SupportConvertDtoToEntity = SupportConvertDtoToEntity()

    def get_description_for_root(self) -> NodeUnitDescription:
        try:
            list_root_node_unit: list[NodeUnit] = self.__SupportGetRootNodes.get_root_nodes()
            root_node_unit: NodeUnit
            if len(list_root_node_unit) > 1:
                raise Exceptions.OperationIncompleteException("Engine incompatible with multiroot graph")
            elif len(list_root_node_unit) == 0:
                raise Exceptions.OperationIncompleteException("Root node not found")
            elif len(list_root_node_unit) < 0:
                raise Exceptions.OperationIncompleteException("Undefined error")
            else:
                root_node_unit = list_root_node_unit[0]
            root_node_unit_description: NodeUnitDescription = self.__SupportConvertDtoToEntity.get_entity(root_node_unit)
            return root_node_unit_description
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

