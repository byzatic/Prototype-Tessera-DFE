#
#
#
import logging
import os
from dotenv import load_dotenv
from src.LibByzaticCommon.Singleton.Singleton import Singleton
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ReadEnvironmentData(Singleton):
    def __init__(self, env_file: str):
        self.logger: logging.Logger = logging.getLogger("base_logger")
        try:
            load_dotenv(dotenv_path=env_file)
            self.__env_value_default: str = ""
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get(self, param_name: str, param_default: str = "") -> str:
        try:
            new_value = os.getenv(param_name, default=self.__env_value_default)
            if new_value == "":
                return param_default
            else:
                return new_value
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __del__(self):
        del self.__env_value_default
