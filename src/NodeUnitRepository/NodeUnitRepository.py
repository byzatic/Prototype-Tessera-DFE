#
#
#
import logging
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.InterfaceNodeUnitDescriptionRepository import InterfaceNodeUnitDescriptionRepository
from Global2p1.InterfaceNodeUnitDescriptionIdRepository import InterfaceNodeUnitDescriptionIdRepository
from src.DaoNodeUnit import DaoNodeUnit
from Global2p1.NodeUnit.NodeUnit import NodeUnit
from Global.NodeUnitDescription import NodeUnitDescription
from src.LibByzaticCommon import Exceptions
from .local_api.InterfaceGetTopLevelNodes import InterfaceGetTopLevelNodes
from .local_api.InterfaceGetRootNode import InterfaceGetRootNode
from .GetTopLevelNodes import GetTopLevelNodes
from .GetRootNodes import GetRootNodes
from .SupportConvertNodeUnitToNodeUnitDescription import SupportConvertNodeUnitToNodeUnitDescription


class NodeUnitRepository(InterfaceNodeUnitRepository, InterfaceNodeUnitDescriptionRepository, InterfaceNodeUnitDescriptionIdRepository):
    __DaoGraphData: DaoNodeUnit

    def __init__(self, dao_graph_data: DaoNodeUnit):
        self.__logger: logging.Logger = logging.getLogger("NodeUnitRepository-logger")
        self.__DaoGraphData: DaoNodeUnit = dao_graph_data
        self.__GetTopLevelNodes: InterfaceGetTopLevelNodes = GetTopLevelNodes()
        self.__GetRootNodes: InterfaceGetRootNode = GetRootNodes()
        self.__SupportConvertNodeUnitToNodeUnitDescription: SupportConvertNodeUnitToNodeUnitDescription = SupportConvertNodeUnitToNodeUnitDescription()

    def get_node_unit(self, description_entity: NodeUnitDescription) -> NodeUnit:
        try:
            node_id: str = description_entity.get_node_id()
            self.__logger.debug(f"get_node_unit: Try to get node unit by id: {node_id}")
            node_unit: NodeUnit = self.__DaoGraphData.get_node_unit(node_id)
            return node_unit
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def get_all_node_unit(self) -> list[NodeUnit]:
        all_id: list[str] = self.__DaoGraphData.get_all_node_id()
        list_dto: list[NodeUnit] = []
        for node_id in all_id:
            node_unit: NodeUnit = self.__DaoGraphData.get_node_unit(node_id)
            list_dto.append(node_unit)
        return list_dto

    def get_root_node_unit(self) -> NodeUnit:
        return self.__GetRootNodes.get_root_node(self.get_all_node_unit())

    def get_top_level_node_units(self) -> list[NodeUnit]:
        return self.__GetTopLevelNodes.get_top_level_nodes(self.get_all_node_unit())

    #
    def get_node_unit_description_by_id(self, identification_name: str) -> NodeUnitDescription:
        node_unit: NodeUnit = self.__DaoGraphData.get_node_unit(identification_name)
        return self.__SupportConvertNodeUnitToNodeUnitDescription.get_entity(node_unit)

    #
    def get_node_unit_description(self, node_unit: NodeUnit) -> NodeUnitDescription:
        node_unit_description: NodeUnitDescription = self.__SupportConvertNodeUnitToNodeUnitDescription.get_entity(node_unit)
        return node_unit_description

    def get_all_node_unit_description(self) -> list[NodeUnitDescription]:
        list_node_unit: list[NodeUnit] = self.get_all_node_unit()
        list_node_unit_description: list[NodeUnitDescription] = []
        for node_unit in list_node_unit:
            node_unit_description: NodeUnitDescription = self.__SupportConvertNodeUnitToNodeUnitDescription.get_entity(node_unit)
            list_node_unit_description.append(node_unit_description)
        return list_node_unit_description

    def get_root_node_unit_description(self) -> NodeUnitDescription:
        return self.__SupportConvertNodeUnitToNodeUnitDescription.get_entity(self.__GetRootNodes.get_root_node(self.get_all_node_unit()))

    def get_top_level_node_unit_descriptions(self) -> list[NodeUnitDescription]:
        list_node_unit: list[NodeUnit] = self.get_top_level_node_units()
        list_node_unit_description: list[NodeUnitDescription] = []
        for node_unit in list_node_unit:
            node_unit_description: NodeUnitDescription = self.__SupportConvertNodeUnitToNodeUnitDescription.get_entity(node_unit)
            list_node_unit_description.append(node_unit_description)
        return list_node_unit_description
