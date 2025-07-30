#
#
#
from abc import ABCMeta, abstractmethod
from Global2p2.i_StorageItem import i_StorageItem


class i_Storage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, key: str, value: i_StorageItem) -> None:
        pass

    @abstractmethod
    def read(self, key: str) -> i_StorageItem:
        pass

    @abstractmethod
    def update(self, key: str, value: i_StorageItem) -> int:
        pass

    @abstractmethod
    def delete(self, key: str) -> int:
        pass

    @abstractmethod
    def drop(self) -> int:
        pass

    @abstractmethod
    def read_all(self) -> dict:
        pass

    @abstractmethod
    def read_list_keys(self) -> list:
        pass

    @abstractmethod
    def contains(self, key: str) -> bool:
        pass
