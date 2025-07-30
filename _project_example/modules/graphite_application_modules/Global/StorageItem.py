#
#
#
from Global2p2.i_StorageItem import i_StorageItem
from .StorageItemValue import StorageItemValue

class StorageItem(i_StorageItem):
    def __init__(self, name: str, value: StorageItemValue):
        self.__name: str = name
        self.__value: StorageItemValue = value

    def getName(self) -> str:
        return self.__name

    def getValue(self) -> StorageItemValue:
        return self.__value
