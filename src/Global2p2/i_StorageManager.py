#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from Global2p2.i_Storage import i_Storage
from Global.NodeUnitDescription import NodeUnitDescription
from typing import Optional


class i_StorageManager(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_storage(self, storage_name: str, nodeunit_description: Optional[NodeUnitDescription] = None) -> i_Storage:
        pass

    @abstractmethod
    def remove_storage(self, storage_name: str, nodeunit_description: Optional[NodeUnitDescription] = None) -> None:
        pass

    @abstractmethod
    def put_storage(self, storage_name: str, storage_unit: i_Storage, nodeunit_description: Optional[NodeUnitDescription] = None) -> None:
        pass

    @abstractmethod
    def recreate_storages(self) -> None:
        pass
