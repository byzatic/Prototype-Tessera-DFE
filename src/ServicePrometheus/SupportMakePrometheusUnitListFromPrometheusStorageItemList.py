#
#
#
import logging

from Global2p2.i_StorageItem import i_StorageItem
from AdditionalPackages.ApiPrometheus import ApiPrometheusUnitInterface
from AdditionalPackages.ApiPrometheus import ApiPrometheusUnit, ApiPrometheusUnitLabel
from modules.graphite_application_modules.Global.StorageItem import StorageItem
from modules.graphite_application_modules.Global.StorageItemValue import StorageItemValue
from modules.graphite_application_modules.Global.LabelParser.LabelParser import LabelParser
from modules.graphite_application_modules.Global.LabelParser.DtoLabel import DtoLabel

from LibByzaticCommon import Exceptions


class SupportMakePrometheusUnitListFromPrometheusStorageItemList(object):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("ServicePrometheus-logger")
        self.__LabelParser: LabelParser = LabelParser()

    def convert(self, storage_items_list: list[i_StorageItem], metric_name: str) -> list[ApiPrometheusUnitInterface]:
        try:
            prometheus_unit_list: list[ApiPrometheusUnitInterface] = []
            for storage_item in storage_items_list:
                if isinstance(storage_item, StorageItem):
                    storage_item_value_unit: StorageItemValue = storage_item.getValue()
                    storage_item_value: str = storage_item_value_unit.getValue()
                    storage_item_tag_list: list[str] = storage_item_value_unit.getLabel()
                    prometheus_unit_metric_labels_list: list[ApiPrometheusUnitLabel] = self.__convert_storage_item_tag_list_to_prometheus_unit_metric_labels_list(storage_item_tag_list)
                    prometheus_unit: ApiPrometheusUnit = ApiPrometheusUnit(
                        metric_name=storage_item.getName(),
                        metric_value=storage_item_value,
                        metric_labels=prometheus_unit_metric_labels_list
                    )
                    prometheus_unit_list.append(prometheus_unit)
                else:
                    raise Exceptions.OperationIncompleteException(f"Incorrect data type")
            return prometheus_unit_list
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __convert_storage_item_tag_list_to_prometheus_unit_metric_labels_list(self, storage_item_tag_list: list[str]) -> list[ApiPrometheusUnitLabel]:
        try:
            prometheus_unit_metric_labels_list: list[ApiPrometheusUnitLabel] = []
            for storage_item_tag in storage_item_tag_list:
                dto_storage_item: DtoLabel = self.__LabelParser.struct(storage_item_tag)
                prometheus_unit_metric_label: ApiPrometheusUnitLabel = ApiPrometheusUnitLabel(
                    label_value=dto_storage_item.getLabelValue(),
                    label_key=dto_storage_item.getLabelName(),
                    label_sign=dto_storage_item.getLabelSign()
                )
                prometheus_unit_metric_labels_list.append(prometheus_unit_metric_label)
            return prometheus_unit_metric_labels_list
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)