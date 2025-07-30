#
#
#
import logging
from Global2p2.i_StorageItem import i_StorageItem
from modules.graphite_application_modules.Global.StorageItem import StorageItem
from modules.graphite_application_modules.Global.StorageItemValue import StorageItemValue


class SuportCreatorStorageItem(object):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("Workers-PrometheusGetData-logger")

    def create_StorageItem(self, name: str, value: str, labels: list[str]) -> i_StorageItem:
        value_object: StorageItemValue = StorageItemValue(
            value=value,
            label=labels
        )
        storage_item_object: StorageItem = StorageItem(
            name=name,
            value=value_object
        )
        return storage_item_object
