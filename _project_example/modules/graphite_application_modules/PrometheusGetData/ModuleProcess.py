#
#
#
import logging
from typing import Optional
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from Global2p2.i_StorageManager import i_StorageManager
from AdditionalPackages.DaoPrometheus.DaoPrometheus import DaoPrometheus
from AdditionalPackages.DaoPrometheus.ABCAbstractCollection.DaoPrometheusInterface import DaoPrometheusInterface
from AdditionalPackages.DaoPrometheus.PrometheusDto import i_DtoPrometheusMetric, i_DtoPrometheusMetricLabel
from AdditionalPackages.DaoPrometheus.PrometheusDto import impl_DtoPrometheusMetric, impl_DtoPrometheusMetricLabel
from AdditionalPackages.DaoPrometheusQueryConfigurations.i_DaoPrometheusQueryConfigurations import i_DaoPrometheusQueryConfigurations
from AdditionalPackages.DaoPrometheusQueryConfigurations.impl_DaoPrometheusQueryConfigurations import impl_DaoPrometheusQueryConfigurations
from DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration.PrometheusQueryConfiguration import PrometheusQueryConfiguration
from Global.NodeUnitDescription import NodeUnitDescription
from ServicePrometheus.i_WorkerContext import i_WorkerContext
from Global2p2.i_Storage import i_Storage
from Global2p2.i_StorageItem import i_StorageItem
from .SuportCreatorStorageItem import SuportCreatorStorageItem
from .SupportConvertPrometheusQueryConfigurationToPrometheusQueryUnit import SupportConvertPrometheusQueryConfigurationToPrometheusQueryUnit
from LibByzaticCommon import Exceptions


class ModuleProcess(object):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-PrometheusGetData-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self._storage_manager: i_StorageManager = self._application_context.getStorageManager()
        self.__DaoPrometheus: DaoPrometheusInterface
        self.__DaoPrometheusQueryConfigurations: i_DaoPrometheusQueryConfigurations
        self.__SupportCreatorStorageItem: SuportCreatorStorageItem = SuportCreatorStorageItem()
        self.__SupportConvertPrometheusQueryConfigurationToPrometheusQueryUnit: SupportConvertPrometheusQueryConfigurationToPrometheusQueryUnit = SupportConvertPrometheusQueryConfigurationToPrometheusQueryUnit()
        self.__init_prometheus_query_engine()

    def __init_prometheus_query_engine(self):
        try:
            self.__DaoPrometheus = DaoPrometheus()
            prometheus_query_configurations_config_file: Optional[str] = None
            for parameter in self._abstract_data_list:
                if parameter.get_abstract_data_type() == "SubEngineQueryConfigurationFile":
                    prometheus_query_configurations_config_file = parameter.get_abstract_data_specialty()
            if prometheus_query_configurations_config_file is not None and prometheus_query_configurations_config_file != "":
                self.__DaoPrometheusQueryConfigurations = impl_DaoPrometheusQueryConfigurations(prometheus_query_configurations_config_file)
            else:
                raise Exceptions.OperationIncompleteException(f"SubEngineQueryConfigurationFile not set")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)

    def run(self):
        storage: i_Storage = self.__get_output_storage()
        for parameter in self._abstract_data_list:
            if parameter.get_abstract_data_type() == "InputQueryID":
                self.__logger.debug(f"Found parameter InputQueryID with specialty {parameter.get_abstract_data_specialty()}")

                data: i_DtoPrometheusMetric = self.__get_data(parameter)
                self.__logger.debug(f"data received -> {data}")
                storage_item: i_StorageItem = self.__SupportCreatorStorageItem.create_StorageItem(
                    value=data.value,
                    labels=self.__get_output_data_labels(parameter, data.metric_labels),
                    name=self.__get_output_data_name(parameter.get_abstract_data_key())
                )
                self.__logger.debug(f"storage item created")

                storage_item_name: str = self.__get_metric_name(parameter.get_abstract_data_key())
                if not storage.contains(storage_item_name):
                    storage.create(storage_item_name, storage_item)
                    self.__logger.debug(f"data saved")
                else:
                    Exceptions.OperationIncompleteException(f"Internal Worker error: Duplication of metric name -> {storage_item_name}")
        self._storage_manager.put_storage(self.__get_output_storage_name(), storage, self._current_node_description)

    def __get_output_data_name(self, search_for_abstract_data_specialty: str):
        abstract_data_key: Optional[str] = None
        for parameter in self._abstract_data_list:
            if parameter.get_abstract_data_type() == "OutputData" and parameter.get_abstract_data_specialty() == search_for_abstract_data_specialty:
                abstract_data_key = parameter.get_abstract_data_key()
        if abstract_data_key is None:
            raise Exceptions.OperationIncompleteException("abstract_data_key in OutputData is None")
        else:
            return abstract_data_key

    def __get_metric_name(self, search_for_abstract_data_specialty: str):
        metric_name: Optional[str] = None
        for parameter in self._abstract_data_list:
            if parameter.get_abstract_data_type() == "OutputData" and parameter.get_abstract_data_specialty() == search_for_abstract_data_specialty:
                metric_name = parameter.get_abstract_data_specialty()
        if metric_name is None:
            raise Exceptions.OperationIncompleteException("abstract_data_specialty in OutputData is None")
        else:
            return metric_name

    def __get_output_data_labels(self, parameter: NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit, original_list_tags: list[i_DtoPrometheusMetricLabel]) -> list[str]:
        labels_list: list[str] = []

        self_labels_list: list[str] = self.__search_for_output_data_label(parameter.get_abstract_data_key())
        self.__logger.debug(f"Found self labels {self_labels_list}")
        labels_list.extend(self_labels_list)

        filtered_labels_list: list[str] = []
        filter_operating_mode: str = self.__get_OutputDataLabelFilterOperatingMode(parameter.get_abstract_data_key())
        if filter_operating_mode == "RejectAll":
            filtered_labels_object_list: list[i_DtoPrometheusMetricLabel] = self.__filter_OperatingMode_RejectAll(original_list_tags, self.__get_list_allowed_tag_keys(parameter.get_abstract_data_key()))
            for filtered_label in filtered_labels_object_list:
                str_label: str = "{" + filtered_label.key + filtered_label.sign + filtered_label.value + "}"
                self.__logger.debug(f"Allowed label {str_label}")
                filtered_labels_list.append(str_label)
        else:
            raise Exceptions.OperationIncompleteException(f"Undefined filter operating mode {filter_operating_mode}")
        labels_list.extend(filtered_labels_list)

        return labels_list

    def __get_OutputDataLabelFilterOperatingMode(self, search_for_abstract_data_specialty: str) -> str:
        self.__logger.debug(f"search for OutputDataLabelFilterOperatingMode value with specialty {search_for_abstract_data_specialty}")
        output_data_label_filter_operating_mode: Optional[str] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputDataLabelFilterOperatingMode" and abstract_data.get_abstract_data_specialty() == search_for_abstract_data_specialty:
                output_data_label_filter_operating_mode = abstract_data.get_abstract_data_value()
                break
        if output_data_label_filter_operating_mode is not None:
            return output_data_label_filter_operating_mode
        else:
            raise Exceptions.OperationIncompleteException(f"OutputDataLabelFilterOperatingMode not found")

    def __filter_OperatingMode_RejectAll(self, original_list_tags: list[i_DtoPrometheusMetricLabel], list_allowed_tag_keys: list[str]):
        new_list_tags: list[i_DtoPrometheusMetricLabel] = []
        for tag in original_list_tags:
            if tag.key in list_allowed_tag_keys:
                new_list_tags.append(tag)
        return new_list_tags

    def __get_list_allowed_tag_keys(self, search_for_abstract_data_specialty: str):
        list_allowed_tag_keys: list[str] = []
        for parameter in self._abstract_data_list:
            if parameter.get_abstract_data_type() == "OutputDataLabelFilter" and parameter.get_abstract_data_specialty() == search_for_abstract_data_specialty:
                label_value = parameter.get_abstract_data_value()
                list_allowed_tag_keys.append(label_value)
        if list_allowed_tag_keys == []:
            self.__logger.warning(f"labels not found")
            return []
        else:
            self.__logger.warning(f"OutputDataLabelFilter found {list_allowed_tag_keys}")
            return list_allowed_tag_keys

    def __search_for_output_data_label(self, search_for_abstract_data_specialty: str) -> list[str]:
        labels_list: list[str] = []
        for parameter in self._abstract_data_list:
            if parameter.get_abstract_data_type() == "OutputDataLabel" and parameter.get_abstract_data_specialty() == search_for_abstract_data_specialty:
                label_value = parameter.get_abstract_data_value()
                labels_list.append(label_value)
        if labels_list == []:
            self.__logger.warning(f"labels not found")
            return []
        else:
            self.__logger.warning(f"labels found {labels_list}")
            return labels_list

    def __get_data(self, parameter: NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit) -> i_DtoPrometheusMetric:
        query_configuration_unit: PrometheusQueryConfiguration = self.__DaoPrometheusQueryConfigurations.getPrometheusQueryConfigurationUnit(parameter.get_abstract_data_specialty())
        self.__logger.debug(f"configuration unit received")
        data: i_DtoPrometheusMetric = self.__DaoPrometheus.get(
            self.__SupportConvertPrometheusQueryConfigurationToPrometheusQueryUnit.convert(query_configuration_unit, parameter.get_abstract_data_specialty()))
        self.__logger.debug(f"data received -> {data.value} | {data.timestamp}")
        data_value: i_DtoPrometheusMetric = self.__postprocessing_set_none_data_response(data)
        self.__logger.debug(f"data returns -> {data_value}")
        return data_value

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

    def __postprocessing_set_none_data_response(self, data: i_DtoPrometheusMetric) -> i_DtoPrometheusMetric:
        self.__logger.debug(f"postprocessing data -> value of data is {data.value}")
        if data.value is None:
            defined_value=f"1"
            self.__logger.debug(f"postprocessing data is None -> value set as {defined_value}")
            data_value_object: i_DtoPrometheusMetric = impl_DtoPrometheusMetric(
                value=defined_value,
                metric_labels=[],
                timestamp=data.timestamp
            )
            return data_value_object
        else:
            return data
