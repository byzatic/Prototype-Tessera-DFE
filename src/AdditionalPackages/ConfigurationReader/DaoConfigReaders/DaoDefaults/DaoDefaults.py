#
#
#
import logging
from src.LibByzaticCommon.Singleton.Singleton import Singleton
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueStringStorage import KeyValueStringStorage
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class DaoDefaults(Singleton):
    def __init__(self, defaults: dict):
        self.logger: logging.Logger = logging.getLogger("base_logger")
        self.__defaults: dict = defaults
        try:
            self.__local_storage = KeyValueStringStorage("DaoDefaults_storage")
            self.__local_storage.class_name = str(self.__class__.__name__)
            for default_key, default_value in defaults.items():
                self.__local_storage.create(default_key, default_value)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get(self, param_name: str) -> str:
        try:
            if self.__local_storage.contains(param_name):
                return self.__local_storage.read(param_name)
            else:
                return ""
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get_names_list(self) -> list:
        try:
            return self.__local_storage.read_list_keys()
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __del__(self):
        del self.__local_storage
        del self.__defaults
