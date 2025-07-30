#
#
#
import logging
from typing import Union

from DaoNodeUnit.LocalApi.InterfaceGraphDataConverter import InterfaceGraphDataConverter
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnit
from Global2p1.NodeUnit import NodeUnit
from DaoNodeUnit.NodeUnitStorage import KeyValueDtoNodeUnitStorage
from DaoNodeUnit.NodeIdStorage import KeyValueNodeIdStorage
from .SupportNodeUnitCreator import SupportNodeUnitCreator
from DaoNodeUnit.NodeUnitStorage import DtoNodeUnitStorage

from src.LibByzaticCommon.RandomStringGenerator import RandomStringGenerator, RandomStringGeneratorInterface
from src.LibByzaticCommon import Exceptions


class GraphDataConverter(InterfaceGraphDataConverter):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("DaoNodeUnit-logger")
        self.__NodeUnitStorageName: str = "GraphDataConverter-DtoNodeUnit-storage"
        self.__NodeUnitStorage: KeyValueDtoNodeUnitStorage = KeyValueDtoNodeUnitStorage(self.__NodeUnitStorageName)
        self.__RandomStringGenerator: RandomStringGeneratorInterface = RandomStringGenerator()
        self.__NodeIdStorage: KeyValueNodeIdStorage = KeyValueNodeIdStorage("GraphDataConverter-NodeId-storage")
        self.__SupportNodeUnitCreator: SupportNodeUnitCreator = SupportNodeUnitCreator()

    def convert(self, dto_node_unit: DtoRawGraphDataNodeUnit) -> DtoNodeUnitStorage:
        try:
            self.__convertation(dto_node_unit)
            return self.__NodeUnitStorage.get_storage_dto()
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __convertation(self, dto_node_unit: DtoRawGraphDataNodeUnit, upstream_unit_node_id: Union[str, None] = None):
        node_unit_id: str = self.__RandomStringGenerator.get_token(12)
        self.__logger.debug(f"GraphDataConverter -> __convertation -> node_unit_id is {node_unit_id}")

        new_upstream: list[str] = []
        if upstream_unit_node_id is not None:
            new_upstream: list[str] = [upstream_unit_node_id]
        self.__logger.debug(f"GraphDataConverter -> __convertation -> new_upstream is {new_upstream}")

        downstream: list[DtoRawGraphDataNodeUnit] = dto_node_unit.downstream
        self.__logger.debug(f"GraphDataConverter -> __convertation -> downstream is {downstream}")

        downstream_data: list[str]
        if downstream == []:
            downstream_data: list[str] = []
        else:
            for downstream_item in downstream:
                self.__logger.debug(f"GraphDataConverter -> __convertation -> "
                                    f"call recursive for {downstream_item} {node_unit_id}")
                self.__convertation(downstream_item, node_unit_id)
            downstream_data = self.__NodeIdStorage.read(node_unit_id)
        new_dto_node_unit: NodeUnit = self.__SupportNodeUnitCreator.create_node_unit_from_node_raw(
            dto_raw_graph_data_node_unit=dto_node_unit,
            upstream=new_upstream,
            downstream=downstream_data,
            node_id=node_unit_id
        )
        self.__logger.debug(f"GraphDataConverter -> __convertation -> dto_node_unit created")
        self.__NodeUnitStorage.create(node_unit_id, new_dto_node_unit)
        self.__logger.debug(f"GraphDataConverter -> __convertation -> dto_node_unit saved with id {node_unit_id}")
        if upstream_unit_node_id is not None:
            self.__put_node_in_upstream(upstream_unit_node_id, node_unit_id)

    def __put_node_in_upstream(self, upstream_unit_id: str, downstream_unit_id: str):
        if self.__NodeIdStorage.contains(upstream_unit_id):
            upstream: list[str] = self.__NodeIdStorage.read(upstream_unit_id)
            upstream.append(downstream_unit_id)
            self.__NodeIdStorage.update(upstream_unit_id, upstream)
            self.__logger.debug(f"GraphDataConverter -> __put_node_in_upstream -> "
                                f"update  node_unit_id: {upstream_unit_id} "
                                f"with upstream {downstream_unit_id}")
        else:
            self.__NodeIdStorage.create(upstream_unit_id, [downstream_unit_id])
            self.__logger.debug(f"GraphDataConverter -> __put_node_in_upstream -> "
                                f"create  node_unit_id: {upstream_unit_id} "
                                f"with upstream {downstream_unit_id}")
