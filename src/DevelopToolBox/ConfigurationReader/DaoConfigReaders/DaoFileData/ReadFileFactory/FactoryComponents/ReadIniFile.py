#
#
#
import logging
from configparser import ConfigParser
from src.LibByzaticCommon.FileReaders.ConfigParserFileReader import ConfigParserFileReader
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from src.LibByzaticCommon.Flattener.ConfigParserFlattener.ConfigParserFlattener import ConfigParserFlattener
from src.DevelopToolBox.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileFactory.FactoryComponents.Abstract import AbstractFactoryComponent


class ReadIniFile(AbstractFactoryComponent):
    def __init__(self, path: str):
        self.logger: logging.Logger = logging.getLogger("ConfigurationReader_logger")
        self.__path: str = path
        self.__reader: ConfigParserFileReader = ConfigParserFileReader()
        self.configparser_flattener = ConfigParserFlattener()

    def read(self) -> dict:
        try:
            self.logger.debug(f"read ini from file {self.__path}")
            data: ConfigParser = self.__reader.read(self.__path)
            flatten_data: dict = self.configparser_flattener.flatten(data)
            self.logger.debug(f"flatten data from ini file is -> {self.__path}")
            return flatten_data
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)
