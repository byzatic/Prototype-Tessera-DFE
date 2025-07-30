#
# Defaults -> File Configs -> Environment -> System Environment -> Command Line Arguments
#
import logging
from src.LibByzaticCommon.Singleton.Singleton import Singleton
from src.ApplicationCommon.ConfigurationReader.DaoConfigReaders.DaoDefaults.DaoDefaults import DaoDefaults
from src.ApplicationCommon.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileData import ReadFileData
from src.ApplicationCommon.ConfigurationReader.DaoConfigReaders.DaoEnvironmentData.ReadEnvironmentData import ReadEnvironmentData
from src.ApplicationCommon.ConfigurationReader.DaoConfigReaders.DaoCommandLineArguments.ReadCommandLineArguments import ReadCommandLineArguments
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueStringStorage import KeyValueStringStorage
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ConfigurationRepository(Singleton):
    def __init__(self, defaults: dict, env_file: str, config_file: str, config_file_type: str):
        """
        Defaults -> File Configs -> Environment (.env) -> System Environment -> Command Line Arguments
        """
        self.logger: logging.Logger = logging.getLogger("ConfigurationReader_logger")
        #
        try:
            self.__defaults_dao = DaoDefaults(defaults)
            self.__environment_dao = ReadEnvironmentData(env_file)
            self.__file_dao = ReadFileData(config_file, config_file_type)
            self.__command_line_arguments_dao = ReadCommandLineArguments()
            #
            self.__local_storage = KeyValueStringStorage("ConfigurationRepository_storage")
            #
            self.__parameters_list = self.__defaults_dao.get_names_list()
            self.__calculate_parameters()
            self.__remove_dao()
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get(self, parameter_name: str) -> str:
        try:
            if self.__local_storage.contains(parameter_name):
                return self.__local_storage.read(parameter_name)
            else:
                raise OperationIncompleteException(f"No such parameter name {parameter_name}")
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

    def __calculate_parameters(self):
        try:
            for parameter_name in self.__parameters_list:
                parameter_defaults: str = self.__defaults_dao.get(parameter_name)
                calculated_parameter_file: str = self.__file_dao.get(parameter_name, parameter_defaults)
                calculated_parameter_environment: str = self.__environment_dao.get(parameter_name, calculated_parameter_file)
                calculated_parameter_command_line: str = self.__command_line_arguments_dao.get(parameter_name, calculated_parameter_environment)
                calculated_parameter: str = calculated_parameter_command_line
                self.__local_storage.create(parameter_name, calculated_parameter)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __remove_dao(self):
        del self.__defaults_dao
        del self.__environment_dao
        del self.__file_dao
        del self.__command_line_arguments_dao
