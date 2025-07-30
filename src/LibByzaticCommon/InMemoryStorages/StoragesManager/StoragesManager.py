#!/usr/bin/env python3
#
# ========= Interfaces =========
#
#
#
#
import logging
from src.LibByzaticCommon.Singleton.Singleton import Singleton
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
#
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueStoragesStorage import KeyValueStoragesStorage
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueStringStorage import KeyValueStringStorage
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueDictStorage import KeyValueDictStorage
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueObjectStorage import KeyValueObjectStorage
#
from src.LibByzaticCommon.InMemoryStorages.ABCAbstractCollection import KeyValueObjectStorageInterface, \
    KeyValueStoragesStorageInterface, KeyValueDictStorageInterface, KeyValueStorageInterface, \
    KeyValueStringStorageInterface


class StoragesManager(Singleton):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("basic_logger")
        self.__storage: KeyValueStringStorageInterface = KeyValueStoragesStorage("StorageManager_storage", True)

    def get(self, storage_type: KeyValueStorageInterface, storage_name: str, critical_dump_flag: bool = True) \
            -> KeyValueStorageInterface:
        """
        Native Byzatic storage manager
        @param storage_type: instance of KeyValueStorageInterface
        (look at LibByzaticCommon.NodeStorage.ABCAbstractCollection.Readers)
        @param storage_name: name of storage
        @param critical_dump_flag: True by default or False
        @return: instance of KeyValueStorageInterface
        """
        try:
            storage: KeyValueStorageInterface
            if isinstance(storage_type, KeyValueDictStorageInterface.KeyValueDictStorageInterface):
                return self.__keyvaluedictstorage_init(storage_name, critical_dump_flag)
            elif isinstance(storage_type, KeyValueObjectStorageInterface.KeyValueObjectStorageInterface):
                return self.__keyvalueobjectstorage_init(storage_name, critical_dump_flag)
            elif isinstance(storage_type, KeyValueStoragesStorageInterface.KeyValueStoragesStorageInterface):
                return self.__keyvaluestringstorage_init(storage_name, critical_dump_flag)
            else:
                raise OperationIncompleteException(f"StoragesManager: requested storage type is not an "
                                          f"instance of AbstractKeyValueStorage")
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __keyvaluedictstorage_init(self, storage_name: str, critical_dump_flag: bool = True):
        storage: KeyValueStorageInterface
        if self.__storage.contains(storage_name):
            storage = self.__storage.read(storage_name)
            if isinstance(storage, KeyValueDictStorageInterface.KeyValueDictStorageInterface):
                pass
            else:
                raise OperationIncompleteException(f"StoragesManager: requested storage is not a "
                                          f"type of AbstractKeyValueDictStorage")
            self.__logger.debug(f"Storage with name {storage_name} already exists, return {storage_name}")
        else:
            storage = KeyValueDictStorage(storage_name, critical_dump_flag)
            self.__storage.create(storage_name, storage)
            self.__logger.debug(f"Created instance of AbstractKeyValueDictStorage storage: {storage_name}")
        return storage

    def __keyvalueobjectstorage_init(self, storage_name: str, critical_dump_flag: bool = True):
        storage: KeyValueStorageInterface
        if self.__storage.contains(storage_name):
            storage = self.__storage.read(storage_name)
            if isinstance(storage, KeyValueObjectStorageInterface.KeyValueObjectStorageInterface):
                pass
            else:
                raise OperationIncompleteException(f"StoragesManager: requested storage is not a "
                                          f"type of AbstractKeyValueObjectStorage")
            self.__logger.debug(f"Storage with name {storage_name} already exists, return {storage_name}")
        else:
            storage = KeyValueObjectStorage(storage_name, critical_dump_flag)
            self.__storage.create(storage_name, storage)
            self.__logger.debug(f"Created instance of AbstractKeyValueDictStorage storage: {storage_name}")
        return storage

    def __keyvaluestringstorage_init(self, storage_name: str, critical_dump_flag: bool = True):
        storage: KeyValueStringStorageInterface
        if self.__storage.contains(storage_name):
            storage = self.__storage.read(storage_name)
            if isinstance(storage, KeyValueStringStorageInterface.KeyValueStringStorageInterface):
                pass
            else:
                raise OperationIncompleteException(f"StoragesManager: requested storage is not a "
                                          f"type of AbstractKeyValueObjectStorage")
            self.__logger.debug(f"Storage with name {storage_name} already exists, return {storage_name}")
        else:
            storage = KeyValueStringStorage(storage_name, critical_dump_flag)
            self.__storage.create(storage_name, storage)
            self.__logger.debug(f"Created instance of AbstractKeyValueDictStorage storage: {storage_name}")
        return storage
