#
#
#
import logging
from typing import Optional
from time import sleep
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from Global2p2.i_StorageManager import i_StorageManager
from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.NodeUnit.NodeUnit import NodeUnit
from ServicePrometheus.i_WorkerContext import i_WorkerContext
from Global2p2.i_Storage import i_Storage
from Global2p2.i_StorageItem import i_StorageItem
from modules.graphite_application_modules.Global.StorageItem import StorageItem
from modules.graphite_application_modules.Global.StorageItemValue import StorageItemValue
from Global2p3.i_GraphAnalytics import i_GraphAnalytics
from GraphAnalytics.impl_GraphAnalytics import impl_GraphAnalytics
from LibByzaticCommon import Exceptions


class ModuleProcess(object):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-ModuleAddGraphPath-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self._storage_manager: i_StorageManager = self._application_context.getStorageManager()
        self.__GraphAnalytics: i_GraphAnalytics = impl_GraphAnalytics(self._application_context.getNodeUnitRepository())
        self.__metrics_abstract_key_path_tag: str = self.__get_metrics_abstract_key_path_tag()

    def run(self):
        input_storage: i_Storage = self.__get_input_storage()
        output_storage: i_Storage = self.__get_output_storage()
        for abstract in self._abstract_data_list:
            if abstract.get_abstract_data_type() == "InputData":
                self.__logger.debug(f"found abstract data of type InputData with abstract_data_specialty -> {abstract.get_abstract_data_specialty()}")
                input_storage_item: i_StorageItem = input_storage.read(abstract.get_abstract_data_specialty())
                calculated_path_tag: str = self.__metrics_abstract_key_path_tag
                if isinstance(input_storage_item, StorageItem):
                    new_labels_list: list[str] = input_storage_item.getValue().getLabel()
                    new_labels_list.append(calculated_path_tag)
                    self.__logger.debug(f"generated new labels list {new_labels_list}")
                    new_input_storage_item_value: StorageItemValue = StorageItemValue(
                        value=input_storage_item.getValue().getValue(),
                        label=new_labels_list
                    )
                    new_input_storage_item: StorageItem = StorageItem(
                        name=input_storage_item.getName(),
                        value=new_input_storage_item_value
                    )
                    self.__logger.debug(f"Storage item created")
                    input_storage.update(abstract.get_abstract_data_specialty(), new_input_storage_item)
                    self.__logger.debug(f"Storage item updated")

                    # ----- DEBUG
                    # check_update: i_StorageItem = input_storage.read(abstract.get_abstract_data_specialty())
                    # if isinstance(check_update, StorageItem):
                    #     self.__logger.debug(f"check_update labels {check_update.getValue().getLabel()}")
                    # else:
                    #     raise Exceptions.OperationIncompleteException(f"storage item is wrong type")

                else:
                    raise Exceptions.OperationIncompleteException(f"storage item is wrong type")
        self._storage_manager.put_storage(self.__get_input_storage_name(), input_storage, self._current_node_description)
        self.__logger.debug(f"Storage saved")

        # ----- DEBUG
        # for abstract in self._abstract_data_list:
        #     if abstract.get_abstract_data_type() == "InputData":
        #         check_put_storage: i_StorageItem = self._storage_manager.get_storage(self.__get_output_storage_name(), self._current_node_description).read(abstract.get_abstract_data_specialty())
        #         if isinstance(check_put_storage, StorageItem):
        #             self.__logger.debug(f"check_put_storage labels {check_put_storage.getValue().getLabel()}")
        #         else:
        #             raise Exceptions.OperationIncompleteException(f"storage item is wrong type")

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

    def __get_metrics_abstract_key_path_tag(self) -> str:
        node_path: list[NodeUnitDescription] = self.__GraphAnalytics.get_path_from_source_node_to_root_node(self._current_node_description, self._application_context.getRootNodeUnitDescription())
        reversed_node_path: list[NodeUnitDescription] = self.__GraphAnalytics.reverse_path(node_path)
        self.__logger.debug(f"reversed node path contains {len(reversed_node_path)} items")

        metrics_abstract_key_path: list[str] = []
        for node_path_item in reversed_node_path:
            self.__logger.debug(f"search for node item {node_path_item.get_node_id()}")
            result_of_searching_processing_status: bool = False
            result_of_searching_output_data: bool = False
            node_path_item_node_unit: NodeUnit = self._application_context.getNodeUnitRepository().get_node_unit(node_path_item)
            for stages_info in node_path_item_node_unit.get_workers_pipeline().get_stages_description().get_stages_info():
                if stages_info.get_stage_id() == "ProcessingStatus":
                    self.__logger.debug(f"Found {node_path_item.get_node_id()} -> ProcessingStatus")
                    for stage_data in stages_info.get_stage_data():
                        if stage_data.get_name() == "ModuleProcessingStatus":
                            self.__logger.debug(f"Found {node_path_item.get_node_id()} -> ProcessingStatus -> ModuleProcessingStatus")
                            result_of_searching_processing_status = True
                            for abstract_data in stage_data.get_abstract_data_list():
                                if abstract_data.get_abstract_data_type() == "OutputData":
                                    self.__logger.debug(f"Found {node_path_item.get_node_id()} -> ProcessingStatus -> ModuleProcessingStatus -> OutputData")
                                    result_of_searching_output_data = True
                                    metrics_abstract_key_path.append(abstract_data.get_abstract_data_key())
            if not result_of_searching_processing_status:
                self.__logger.error(f"processing status not found")
                raise Exceptions.OperationIncompleteException(f"processing status not found")
            if not result_of_searching_output_data:
                self.__logger.error(f"output data not found")
                raise Exceptions.OperationIncompleteException(f"output data not found")
        if len(node_path) != len(metrics_abstract_key_path):
            raise Exceptions.OperationIncompleteException(f"error in path convertation")
        else:
            path_tag: str = "{path="
            for metrics_abstract_key_path_item in metrics_abstract_key_path:
                path_tag = path_tag + metrics_abstract_key_path_item + "."
            path_tag = path_tag[:-1] + "}"
            self.__logger.debug(f"generated path tag {path_tag}")
            return path_tag
