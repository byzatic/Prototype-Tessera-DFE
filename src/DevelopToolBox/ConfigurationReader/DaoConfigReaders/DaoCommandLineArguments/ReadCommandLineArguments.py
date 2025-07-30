#
#
#
import logging
from src.LibByzaticCommon.Singleton.Singleton import Singleton
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ReadCommandLineArguments(Singleton):
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger("base_logger")

    def get(self, param_name: str, param_default: str = "") -> str:
        new_value: str = ""
        if new_value == "":
            return param_default
        else:
            return new_value

    def __del__(self):
        try:
            pass
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)
