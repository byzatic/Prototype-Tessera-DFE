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
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.InterfaceNodeUnitDescriptionIdRepository import InterfaceNodeUnitDescriptionIdRepository
from Global2p1.NodeUnit import NodeUnit, NodeUnitOption
from Global2p2.i_StorageItem import i_StorageItem
from LibByzaticCommon import Exceptions


class ModuleProcess(object):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-ModuleLiftingData-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self._storage_manager: i_StorageManager = self._application_context.getStorageManager()
        self._node_unit_repository: InterfaceNodeUnitRepository = self._application_context.getNodeUnitRepository()
        self._node_unit_description_id_repository: InterfaceNodeUnitDescriptionIdRepository = self._application_context.getNodeUnitRepository()

    def run(self):
        input_storage_name: str = self.__get_input_storage_name()
        output_storage: i_Storage = self.__get_output_storage()
        node_option_value: str = self.__get_node_option_value()

        input_storage: i_Storage = self.__get_input_storage(input_storage_name, node_option_value)

        lifting_metric_names_list: list[str] = self.__get_lifting_metric_names_list()

        for get_lifting_metric_name in lifting_metric_names_list:
            lifting_metric: i_StorageItem = input_storage.read(get_lifting_metric_name)
            output_storage.create(get_lifting_metric_name, lifting_metric)

        self._storage_manager.put_storage(self.__get_output_storage_name(), output_storage, self._current_node_description)

    def __get_input_storage(self, input_storage_name: str, node_option_value: str) -> i_Storage:
        current_node_unit: NodeUnit = self._node_unit_repository.get_node_unit(self._current_node_description)
        list_id_of_current_node_unit_downstream: list[str] = current_node_unit.get_downstream()
        list_descriptions_of_current_node_unit_downstream: list[NodeUnitDescription] = self.__get_list_descriptions_of_current_node_unit_downstream(list_id_of_current_node_unit_downstream)
        downstream_node_description: NodeUnitDescription = self.__search_node_description_by_node_option_value(list_descriptions_of_current_node_unit_downstream, node_option_value)
        downstream_node_storage: i_Storage = self._storage_manager.get_storage(input_storage_name, downstream_node_description)
        return downstream_node_storage


    def __search_node_description_by_node_option_value(self, list_descriptions_of_current_node_unit_downstream: list[NodeUnitDescription], node_option_value: str) -> NodeUnitDescription:
        result_description: Optional[NodeUnitDescription] = None
        for descriptions_of_current_node_unit_downstream in list_descriptions_of_current_node_unit_downstream:
            node_of_current_node_unit_downstream: NodeUnit = self._node_unit_repository.get_node_unit(descriptions_of_current_node_unit_downstream)
            its_options: list[NodeUnitOption] = node_of_current_node_unit_downstream.get_options()
            for its_option in its_options:
                if its_option.get_option_name() == "NodeName":
                    if its_option.get_option_value() == node_option_value:
                        result_description = descriptions_of_current_node_unit_downstream
        if result_description is not None:
            return result_description
        else:
            raise Exceptions.OperationIncompleteException(f"Node with option NodeName and value {node_option_value} not found")


    def __get_list_descriptions_of_current_node_unit_downstream(self, list_id_of_current_node_unit_downstream: list[str]) -> list[NodeUnitDescription]:
        list_descriptions_of_current_node_unit_downstream: list[NodeUnitDescription] = []
        for id_of_current_node_unit_downstream in list_id_of_current_node_unit_downstream:
            node_unit_description: NodeUnitDescription = self._node_unit_description_id_repository.get_node_unit_description_by_id(id_of_current_node_unit_downstream)
            list_descriptions_of_current_node_unit_downstream.append(node_unit_description)
        if len(list_descriptions_of_current_node_unit_downstream) == len(list_id_of_current_node_unit_downstream):
            return list_descriptions_of_current_node_unit_downstream

    def __get_node_option_value(self) -> str:
        node_option_value: Optional[str] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "NodeOptionsNodeName":
                node_option_value = abstract_data.get_abstract_data_specialty()
                break
        if node_option_value is not None:
            return node_option_value
        else:
            raise Exceptions.OperationIncompleteException(f"abstract data type NodeOptionsNodeName not found")

    def __get_lifting_metric_names_list(self) -> list[str]:
        lifting_metric_names_list: Optional[list[str]] = []
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "LiftingMetric":
                lifting_metric_names_list.append(abstract_data.get_abstract_data_specialty())
        if len(lifting_metric_names_list) > 0:
            return lifting_metric_names_list
        else:
            raise Exceptions.OperationIncompleteException(f"abstract data type LiftingMetric not found")

    def __get_output_storage(self) -> i_Storage:
        output_storage_name: Optional[str] = self.__get_output_storage_name()
        output_storage: i_Storage = self._storage_manager.get_storage(output_storage_name, self._current_node_description)
        self.__logger.debug(f"output storage received")
        return output_storage

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

