#
#
#
import logging
from .ABCAbstractCollection import ApiPrometheusUnitTransformInterface
from ..ApiPrometheusUnit import ApiPrometheusUnitInterface, ApiPrometheusUnitLabelInterface
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ApiPrometheusUnitTransform(ApiPrometheusUnitTransformInterface):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("Application-logger")

    def transform(self, api_prometheus_unit: ApiPrometheusUnitInterface) -> str:
        try:
            self.__check_api_prometheus_unit(api_prometheus_unit)
            metric_string = self.__transform_core(api_prometheus_unit)
            return metric_string
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise OperationIncompleteException(e.args)

    def __transform_core(self, api_prometheus_unit: ApiPrometheusUnitInterface) -> str:
        metric_name: str = api_prometheus_unit.metric_name
        metric_value: str = api_prometheus_unit.metric_value
        metric_labels: list[ApiPrometheusUnitLabelInterface] = api_prometheus_unit.metric_labels
        metric_labels_str: str = self.__generate_label_str(metric_labels)
        metric_string: str = f"{metric_name}{metric_labels_str} {metric_value}"
        return metric_string

    # TODO: make it clever a bit later (look at @1)
    def __generate_label_str(self, api_prometheus_unit_labels: list[ApiPrometheusUnitLabelInterface]) -> str:
        label_str: str = ""
        label_list: list[str] = self.__generate_label_list(api_prometheus_unit_labels)
        for label in label_list:
            label_str = f"{label},{label_str}"
        label_str = "{" + label_str
        replacement = "}"
        label_str = label_str[:-1] + replacement
        return label_str

    # TODO: @1
    # def __generate_label_str(self, buffer, metric_name, metric_tags, metric_value):
    #     tagline_list = []
    #     for tag_structure in metric_tags:
    #         tag_item = str(tag_structure["name"]) + str(tag_structure["sign"]) + "\"" + str(
    #             tag_structure["value"]) + "\""
    #         tagline_list.append(tag_item)
    #     tagline_string = ','.join(str(x) for x in list(tagline_list))
    #     metric = str(metric_name) + "{" + str(tagline_string) + "} " + str(metric_value)
    #     buffer.append(metric)
    #     return (buffer)

    def __generate_label_list(self, api_prometheus_unit_labels: list[ApiPrometheusUnitLabelInterface]) -> list[str]:
        label_list: list[str] = []
        for api_prometheus_unit_label in api_prometheus_unit_labels:
            label_tmp: str = (f"{api_prometheus_unit_label.label_key}"
                              f"{api_prometheus_unit_label.label_sign}"
                              f"\"{api_prometheus_unit_label.label_value}\"")
            label_list.append(label_tmp)
        return label_list

    def __check_api_prometheus_unit(self, api_prometheus_unit: ApiPrometheusUnitInterface):
        metric_name: str = api_prometheus_unit.metric_name
        if metric_name is None:
            self.__logger.error(f"incorrect api_prometheus_unit -> {api_prometheus_unit}")
            raise OperationIncompleteException(f"incorrect api_prometheus_unit -> metric_name is None;"
                                               f" {api_prometheus_unit}")
        metric_value: str = api_prometheus_unit.metric_value
        if metric_value is None:
            self.__logger.error(f"incorrect api_prometheus_unit -> {api_prometheus_unit}")
            raise OperationIncompleteException(f"incorrect api_prometheus_unit -> metric_value is None;"
                                               f" {api_prometheus_unit}")
        metric_labels: list[ApiPrometheusUnitLabelInterface] = api_prometheus_unit.metric_labels
        if metric_labels is None:
            self.__logger.error(f"incorrect api_prometheus_unit -> {api_prometheus_unit}")
            raise OperationIncompleteException(f"incorrect api_prometheus_unit -> metric_labels is None;"
                                               f" {api_prometheus_unit}")
        for api_prometheus_unit_label in api_prometheus_unit.metric_labels:
            label_key: str = api_prometheus_unit_label.label_key
            if label_key is None:
                self.__logger.error(f"incorrect api_prometheus_unit -> {api_prometheus_unit}")
                raise OperationIncompleteException(f"incorrect api_prometheus_unit -> label_key is None;"
                                                   f" {api_prometheus_unit}")
            label_value: str = api_prometheus_unit_label.label_value
            if label_value is None:
                self.__logger.error(f"incorrect api_prometheus_unit -> {api_prometheus_unit}")
                raise OperationIncompleteException(f"incorrect api_prometheus_unit -> label_value is None;"
                                                   f" {api_prometheus_unit}")
            label_sign: str = api_prometheus_unit_label.label_sign
            if label_sign is None:
                self.__logger.error(f"incorrect api_prometheus_unit -> {api_prometheus_unit}")
                raise OperationIncompleteException(f"incorrect api_prometheus_unit -> label_sign is None;"
                                                   f" {api_prometheus_unit}")
