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
from modules.graphite_application_modules.Global.LabelParser.LabelParser import LabelParser
from modules.graphite_application_modules.Global.LabelParser.DtoLabel import DtoLabel


class ModuleProcess(object):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-ModuleAddLabel-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self._storage_manager: i_StorageManager = self._application_context.getStorageManager()
        self.__GraphAnalytics: i_GraphAnalytics = impl_GraphAnalytics(self._application_context.getNodeUnitRepository())
        self.__LabelParser: LabelParser = LabelParser()

    def run(self):
        input_storage: i_Storage = self.__get_input_storage()
        output_storage: i_Storage = self.__get_output_storage()
        for abstract in self._abstract_data_list:
            if abstract.get_abstract_data_type() == "InputData":
                self.__logger.debug(f"found abstract data of type InputData with abstract_data_specialty -> {abstract.get_abstract_data_specialty()}")
                input_storage_item: i_StorageItem = input_storage.read(abstract.get_abstract_data_specialty())
                if isinstance(input_storage_item, StorageItem):
                    new_labels_list: list[str] = input_storage_item.getValue().getLabel()

                    if abstract.get_abstract_data_key() == "Add":
                        new_labels_list.append(abstract.get_abstract_data_value())
                        self.__logger.debug(f"generated new labels list {new_labels_list}")

                    elif abstract.get_abstract_data_key() == "AddIfNotExists":
                        parsed_new_label: DtoLabel = self.__LabelParser.struct(abstract.get_abstract_data_value())
                        label_not_exists: bool = True
                        for label in new_labels_list:
                            parsed_label: DtoLabel = self.__LabelParser.struct(label)
                            if parsed_label.getLabelName() == parsed_new_label.getLabelName():
                                label_not_exists = False
                        if label_not_exists:
                            new_labels_list.append(abstract.get_abstract_data_value())

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
                else:
                    raise Exceptions.OperationIncompleteException(f"storage item is wrong type")
        self._storage_manager.put_storage(self.__get_input_storage_name(), input_storage, self._current_node_description)
        self.__logger.debug(f"Storage saved")

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
