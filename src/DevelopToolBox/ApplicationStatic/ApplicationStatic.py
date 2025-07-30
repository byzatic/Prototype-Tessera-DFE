#
#
#
import logging
import os
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from .ABCAbstractCollection import ApplicationStaticInterface
from src.LibByzaticCommon.InMemoryStorages.KeyValueStorages.KeyValueStringStorage import KeyValueStringStorage
from src.LibByzaticCommon.InMemoryStorages.ABCAbstractCollection.KeyValueStringStorageInterface import KeyValueStringStorageInterface


class ApplicationStatic(ApplicationStaticInterface):
    def __init__(self, file: str):
        self.__logger: logging.Logger = logging.getLogger("ApplicationStatic-logger")
        self.__version = '1.0.4 prototype-2'
        try:
            self.__local_storage: KeyValueStringStorageInterface = KeyValueStringStorage("ApplicationStatic_storage")
            self.__init_data(file)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise OperationIncompleteException(e.args)

    def __init_data(self, file: str) -> None:
        try:
            #
            # SYSTEM_SCRIPT_DIR
            system_script_dir = os.path.abspath(os.path.dirname(file))
            self.__local_storage.create(
                "SYSTEM_SCRIPT_DIR",
                system_script_dir
            )
            #
            # DEFINE_GLOBAL_ENV_FILE_PATH
            define_global_env_file_path = os.path.join(
                system_script_dir,
                '.env'
            )
            self.__local_storage.create(
                "DEFINE_GLOBAL_ENV_FILE_PATH",
                define_global_env_file_path
            )
            #
            # DEFINE_GLOBAL_CONFIG_FILE_PATH_JSON
            define_global_config_file_path_json = os.path.join(
                system_script_dir,
                'configuration',
                'app_configuration.json'
            )
            self.__local_storage.create(
                "DEFINE_GLOBAL_CONFIG_FILE_PATH_JSON",
                define_global_config_file_path_json
            )
            #
            # DEFINE_GLOBAL_CONFIG_FILE_PATH_INI
            define_global_config_file_path_ini = os.path.join(
                system_script_dir,
                'configuration',
                'app_configuration.ini'
            )
            self.__local_storage.create(
                "DEFINE_GLOBAL_CONFIG_FILE_PATH_INI",
                define_global_config_file_path_ini
            )
            #
            # DEFINE_LOGGER_CONFIG_FILE_PATH_JSON
            define_logger_config_file_path_json = os.path.join(
                system_script_dir,
                'configuration',
                'logger_configuration.json'
            )
            self.__local_storage.create(
                "DEFINE_LOGGER_CONFIG_FILE_PATH_JSON",
                define_logger_config_file_path_json
            )
            #
            # APPLICATION_VERSION
            self.__local_storage.create(
                "APPLICATION_VERSION",
                self.__version
            )
            #
            # DEFINE_POLLING_SUBSYSTEM_DATA_JSON_FILE_PATH
            define_polling_subsystem_data_json_file_path = os.path.join(
                system_script_dir,
                'data',
                'new_polling_subsystem_data.json'
            )
            self.__local_storage.create(
                "DEFINE_POLLING_SUBSYSTEM_DATA_JSON_FILE_PATH",
                define_polling_subsystem_data_json_file_path
            )
            #
            # DEFINE_GRAPH_DATA_JSON_FILE_PATH
            define_graph_data_json_file_path = os.path.join(
                system_script_dir,
                'data',
                'graph_data.json'
            )
            self.__local_storage.create(
                "DEFINE_GRAPH_DATA_JSON_FILE_PATH",
                define_graph_data_json_file_path
            )
            #
            # DEFINE_MODULES_DESCRIPTION_JSON_FILE_PATH
            define_modules_description_json_file_path = os.path.join(
                system_script_dir,
                'data',
                'modules_description.json'
            )
            self.__local_storage.create(
                "DEFINE_MODULES_DESCRIPTION_JSON_FILE_PATH",
                define_modules_description_json_file_path
            )

        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise OperationIncompleteException(e.args)

    def get(self, static_name: str) -> str:
        """
        SYSTEM_SCRIPT_DIR \n
        DEFINE_GLOBAL_CONFIG_FILE_PATH_JSON \n
        DEFINE_GLOBAL_ENV_FILE_PATH \n
        DEFINE_LOGGER_CONFIG_FILE_PATH_JSON \n
        DEFINE_MODULES_DESCRIPTION_JSON_FILE_PATH \n
        APPLICATION_VERSION \n
        :param static_name: Name of static parameter
        :return: value of static parameter
        """
        try:
            return self.__local_storage.read(static_name)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise OperationIncompleteException(e.args)

