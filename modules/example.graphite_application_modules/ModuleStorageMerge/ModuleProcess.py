#
#
#
import logging
from typing import Optional
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from Global2p2.i_StorageManager import i_StorageManager
from Global.NodeUnitDescription import NodeUnitDescription
from ServicePrometheus.i_WorkerContext import i_WorkerContext
from Global2p2.i_Storage import i_Storage
from Global2p2.i_StorageItem import i_StorageItem
from LibByzaticCommon import Exceptions


class ModuleProcess(object):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-ModuleStorageMerge-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self._storage_manager: i_StorageManager = self._application_context.getStorageManager()

    def run(self):
        input_storages_list: list[i_Storage] = self.__get_input_storages_list()
        output_storage: i_Storage = self.__get_output_storage()
        for input_storage in input_storages_list:
            list_keys: list[str] = input_storage.read_list_keys()
            for key in list_keys:
                data: i_StorageItem = input_storage.read(key)
                output_storage.create(key, data)
            self.__logger.debug(f"Storage merged")
        self._storage_manager.put_storage(self.__get_output_storage_name(), output_storage, self._current_node_description)

    def __get_input_storages_list(self) -> list[i_Storage]:
        input_storages_list: list[i_Storage] = []
        input_storage_names_list: list[str] = self.__input_storage_names_list()
        for input_storage_name in input_storage_names_list:
            input_storages_list.append(self._storage_manager.get_storage(input_storage_name, self._current_node_description))
        return input_storages_list

    def __input_storage_names_list(self) -> list[str]:
        input_storage_names: Optional[list[str]] = []
        for configuration in self._configuration_list:
            if configuration.get_abstract_data_type() == "InputStorage":
                self.__logger.debug(f"Found input storage {configuration.get_abstract_data_specialty()}")
                input_storage_names.append(configuration.get_abstract_data_specialty())
        if len(input_storage_names) > 0:
            return input_storage_names
        else:
            raise Exceptions.OperationIncompleteException(f"Input storages not found")

    def __get_output_storage(self) -> i_Storage:
        output_storage_name: Optional[str] = self.__get_output_storage_name()
        output_storage: i_Storage = self._storage_manager.get_storage(output_storage_name, self._current_node_description)
        return output_storage

    def __get_output_storage_name(self) -> str:
        output_storage_name: Optional[str] = None
        for configuration in self._configuration_list:
            if configuration.get_abstract_data_type() == "OutputStorage":
                output_storage_name = configuration.get_abstract_data_specialty()
                break
        if output_storage_name is not None:
            return output_storage_name
        else:
            raise Exceptions.OperationIncompleteException(f"Output storage not found")

