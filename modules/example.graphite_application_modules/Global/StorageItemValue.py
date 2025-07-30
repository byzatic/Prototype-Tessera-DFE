#
#
#
from Global2p2.i_StorageItem import i_StorageItem


class StorageItemValue(i_StorageItem):
    def __init__(self, value: str, label: list[str]):
        self.__value: str = value
        self.__label: list[str] = label

    def getValue(self) -> str:
        return self.__value

    def getLabel(self) -> list[str]:
        return self.__label
