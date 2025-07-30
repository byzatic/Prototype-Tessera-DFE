#
#
#
import logging
from src.DevelopToolBox.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileFactory.ReadFileFactory import ReadFileFactory
from src.DevelopToolBox.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileFactory.FactoryComponents.Abstract import AbstractFactoryComponent
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ReadFileData(object):
    def __init__(self, file_path: str, data_type: str):
        """
        DAO class
        :param_name file_path: e.g. "/mydir/myfile.json"
        :param_name data_type: e.g. "json" or "ini"
        """
        self.logger = logging.getLogger("ConfigurationReader_logger")
        self.__data_type = data_type
        self.__file_path = file_path
        self.__factory = ReadFileFactory()
        try:
            self.__reader: AbstractFactoryComponent = self.__factory.get_file_reader(self.__file_path, self.__data_type)
            self.__data = self.__reader.read()
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get(self, param_name: str, param_default: str = "") -> str:
        try:
            if param_name in self.__data:
                return self.__data[param_name]
            else:
                return param_default
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)
