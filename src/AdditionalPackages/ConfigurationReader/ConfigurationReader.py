#
#
#
import logging
from src.LibByzaticCommon.Singleton.Singleton import Singleton
from .ConfigurationRepository.ConfigurationRepository import ConfigurationRepository
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ConfigurationReader(Singleton):
    def __init__(self, defaults: dict, env_file: str, config_file: str, config_file_type: str):
        try:
            self.logger: logging.Logger = logging.getLogger('ConfigurationReader_logger')
            self.__configuration_repository = ConfigurationRepository(defaults, env_file, config_file, config_file_type)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def read_configuration(self):
        try:
            return self.__configuration_repository.get_all()
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)






