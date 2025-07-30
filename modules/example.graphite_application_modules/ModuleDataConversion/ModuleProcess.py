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
from modules.graphite_application_modules.Global.StorageItem import StorageItem
from modules.graphite_application_modules.Global.StorageItemValue import StorageItemValue
from LibByzaticCommon import Exceptions


class ModuleProcess(object):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-ModuleDataConversion-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self._storage_manager: i_StorageManager = self._application_context.getStorageManager()

    def run(self):
        input_storage: i_Storage = self.__get_input_storage()
        output_storage: i_Storage = self.__get_output_storage()

        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "InputData":
                storage_item: i_StorageItem = input_storage.read(abstract_data.get_abstract_data_specialty())
                if isinstance(storage_item, StorageItem):
                    param_output_data: NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit = self.__search_output_data(abstract_data.get_abstract_data_specialty())
                    extension_output_data_label_list: list[str] = self.__search_extension_output_data_label_list(param_output_data.get_abstract_data_key())
                    extension_output_data_label_list.extend(storage_item.getValue().getLabel())
                    new_storage_item_value: StorageItemValue = StorageItemValue(
                        value=storage_item.getValue().getValue(),
                        label=extension_output_data_label_list
                    )
                    new_storage_item: StorageItem = StorageItem(
                        name=storage_item.getName(),
                        value=new_storage_item_value
                    )
                    output_storage.create(param_output_data.get_abstract_data_key(), new_storage_item)
                    self.__logger.debug(f"data saved in output storage")
                else:
                    raise Exceptions.OperationIncompleteException(f"storage item interface type incorrect")
        self._storage_manager.put_storage(self.__get_output_storage_name(), output_storage, self._current_node_description)

    def __search_extension_output_data_label_list(self, abstract_data_specialty: str) -> list[str]:
        output_data_param: list[str] = []
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputDataLabel" and abstract_data.get_abstract_data_specialty() == abstract_data_specialty:
                output_data_param.append(abstract_data.get_abstract_data_value())
                break
        if output_data_param is not None:
            return output_data_param
        else:
            raise Exceptions.OperationIncompleteException(f"Output data not found")

    def __search_output_data(self, abstract_data_specialty: str) -> NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit:
        output_data_param: Optional[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputData" and abstract_data.get_abstract_data_specialty() == abstract_data_specialty:
                output_data_param = abstract_data
                break
        if output_data_param is not None:
            return output_data_param
        else:
            raise Exceptions.OperationIncompleteException(f"Output data not found")

    def __get_input_storage(self) -> i_Storage:
        input_storage_name: Optional[str] = self.__get_input_storage_name()
        input_storage: i_Storage = self._storage_manager.get_storage(input_storage_name, self._current_node_description)
        return input_storage

    def __get_input_storage_name(self) -> str:
        input_storage_name: Optional[str] = None
        for configuration in self._configuration_list:
            if configuration.get_abstract_data_type() == "InputStorage":
                input_storage_name = configuration.get_abstract_data_specialty()
                break
        if input_storage_name is not None:
            return input_storage_name
        else:
            raise Exceptions.OperationIncompleteException(f"Input storage not found")

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

