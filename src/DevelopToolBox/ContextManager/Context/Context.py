#
#
#
import logging

from src.DevelopToolBox.ContextManager.ABCAbstractCollection.ContextInterface import ContextInterface
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueStringStorage import KeyValueStringStorage
from src.LibByzaticCommon.InMemoryStorages.ABCAbstractCollection.KeyValueStringStorageInterface import KeyValueStringStorageInterface
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class Context(ContextInterface):
    def __init__(self, data: dict):
        self.logger: logging.Logger = logging.getLogger('Context-logger')
        try:
            self.__local_storage: KeyValueStringStorageInterface = KeyValueStringStorage("Context_storage")
            self.__local_storage.__logger = self.logger
            for data_key, data_value in data.items():
                self.__local_storage.create(data_key, data_value)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get(self, key: str) -> str:
        try:
            return self.__local_storage.read(key)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get_all(self) -> dict:
        try:
            return self.__local_storage.read_all()
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def contains(self, key: str) -> bool:
        try:
            return self.__local_storage.contains(key)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)
