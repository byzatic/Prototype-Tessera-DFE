#
#
#
# system libs
import logging
import inspect

# project Global
from Global2p1.InterfaceDaoNodeUnit import InterfaceDaoNodeUnit
from Global2p1.NodeUnit import NodeUnit

# module locals
from .GraphDataReader import GraphDataReader
from .LocalApi.InterfaceGraphDataReader import InterfaceGraphDataReader
from .LocalApi.InterfaceGraphDataUnmarshaller import InterfaceGraphDataUnmarshaller
from .GraphDataUnmarshaller import GraphDataUnmarshaller
from .DtoRawGraphData import DtoRawGraphDataNodeUnit
from .NodeUnitStorage import DtoNodeUnitStorage, KeyValueDtoNodeUnitStorage
from .GraphDataConverter import GraphDataConverter

# common
from src.LibByzaticCommon import Exceptions

# Undefined
# . . .


class DaoNodeUnit(InterfaceDaoNodeUnit):
    def __init__(self, data_file_location: str):
        self.__logger: logging.Logger = logging.getLogger("DaoNodeUnit-logger")
        self.__data_file_location: str = data_file_location
        self.__GraphDataReader: InterfaceGraphDataReader = GraphDataReader()
        self.__GraphDataUnmarshaller: InterfaceGraphDataUnmarshaller = GraphDataUnmarshaller()
        self.__DtoNodeUnitStorage: KeyValueDtoNodeUnitStorage = KeyValueDtoNodeUnitStorage("DaoNodeUnit-storage")
        self.__GraphDataConverter: GraphDataConverter = GraphDataConverter()
        self.__load_data()

    def __load_data(self):
        try:
            self.__logger.debug(f"LOADING DATA: Try to load data")
            raw_json_data: dict = self.__GraphDataReader.read_data(self.__data_file_location)
            self.__logger.debug(f"LOADING DATA: raw data loaded")
            raw_node_unit: DtoRawGraphDataNodeUnit = self.__GraphDataUnmarshaller.unmarshal(raw_json_data)
            self.__logger.debug(f"LOADING DATA: raw data unmarshal returns -> raw node unit")
            dto_node_unit_storage: DtoNodeUnitStorage = self.__GraphDataConverter.convert(raw_node_unit)
            self.__logger.debug(f"LOADING DATA: raw data convert returns -> dto of local node unit storage")
            self.__DtoNodeUnitStorage.load_storage_dto(dto_node_unit_storage)
            self.__logger.debug(f"LOADING DATA: local node unit storage -> dto loaded")
            self.__logger.debug(f"LOADING DATA: Finish to load data")
        except Exceptions.OperationIncompleteException as oie:
            self.__logger.error(f"LOADING DATA: Can't to load data -> {oie.args}")
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            self.__logger.error(f"LOADING DATA: Can't to load data -> {e.args}")
            raise Exceptions.OperationIncompleteException(e.args)

    def get_node_unit(self, node_unit_id: str) -> NodeUnit:
        try:
            self.__logger.debug(f"operation: {str(inspect.currentframe().f_code.co_name)} >> Try to get node unit with id {node_unit_id}")
            if self.__DtoNodeUnitStorage.contains(node_unit_id):
                self.__logger.debug(f"operation: {str(inspect.currentframe().f_code.co_name)} >> Getting node unit with id {node_unit_id} successfully finished")
                return self.__DtoNodeUnitStorage.read(node_unit_id)
            else:
                self.__logger.error(f"operation: {str(inspect.currentframe().f_code.co_name)} >> Getting node unit with id {node_unit_id} "
                                    f"error: storage not contains {node_unit_id}")
                raise Exceptions.OperationIncompleteException(f"DaoNodeUnit: Node with id {node_unit_id} not found")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def get_all_node_id(self) -> list[str]:
        return self.__DtoNodeUnitStorage.read_list_keys()
