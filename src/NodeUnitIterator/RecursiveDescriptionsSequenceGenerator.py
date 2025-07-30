#
#
#
import logging
from copy import deepcopy

from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.NodeUnit import NodeUnit

from .SupportConvertNodeUnitToNodeUnitDescription import SupportConvertNodeUnitToNodeUnitDescription
from .SupportNodeUnitDescriptionGenerator import SupportNodeUnitDescriptionGenerator


class RecursiveDescriptionsSequenceGenerator(object):
    def __init__(self, graph_data_repository: InterfaceNodeUnitRepository):
        self.__logger: logging.Logger = logging.getLogger("NodeUnitIterator-logger")
        self.__GraphDataRepository: InterfaceNodeUnitRepository = graph_data_repository
        self.__ConvertDtoToEntity: SupportConvertNodeUnitToNodeUnitDescription = SupportConvertNodeUnitToNodeUnitDescription()
        self.__EntityGenerator: SupportNodeUnitDescriptionGenerator = SupportNodeUnitDescriptionGenerator()
        self.__descriptions_sequence: list[NodeUnitDescription] = []

    def get_descriptions_sequence(self, root_node: NodeUnit) -> list[NodeUnitDescription]:
        self.__drop_descriptions_sequence()
        self.__generator(root_node)
        return deepcopy(self.__descriptions_sequence)

    def __generator(self, dto_node_unit: NodeUnit) -> None:
        dto_node_unit_downstream: list[str] = dto_node_unit.get_downstream()
        if dto_node_unit_downstream == []:
            entity: NodeUnitDescription = self.__ConvertDtoToEntity.get_entity(dto_node_unit)
            self.__descriptions_sequence.append(entity)
        else:
            for downstream_id in dto_node_unit_downstream:
                entity: NodeUnitDescription = self.__EntityGenerator.get_entity(downstream_id)
                downstream_dto_node_unit: NodeUnit = self.__GraphDataRepository.get_node_unit(entity)
                self.__generator(downstream_dto_node_unit)
            entity: NodeUnitDescription = self.__ConvertDtoToEntity.get_entity(dto_node_unit)
            self.__descriptions_sequence.append(entity)

    def __drop_descriptions_sequence(self):
        self.__descriptions_sequence = []


