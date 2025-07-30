#
#
#
import logging
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from src.DevelopToolBox.ContextManager.ABCAbstractCollection.ContextManagerInterface import ContextManagerInterface
from src.DevelopToolBox.ContextManager.ABCAbstractCollection.ContextInterface import ContextInterface
from src.DevelopToolBox.ConfigurationReader import ConfigurationReader
from .Context.Context import Context


class ContextManager(ContextManagerInterface):
    def __init__(self, defaults: dict, env_file: str, config_file: str, config_file_type: str):
        self.logger: logging.Logger = logging.getLogger('ContextManager-logger')
        try:
            self.__configuration_reader = ConfigurationReader(
                defaults,
                env_file,
                config_file,
                config_file_type
            )
            self.__context: ContextInterface = Context(self.__configuration_reader.read_configuration())
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get(self) -> ContextInterface:
        try:
            return self.__context
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)
