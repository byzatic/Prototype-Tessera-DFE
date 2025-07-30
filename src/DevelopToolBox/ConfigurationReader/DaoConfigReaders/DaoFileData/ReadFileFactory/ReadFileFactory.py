#
#
#
import logging
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from src.DevelopToolBox.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileFactory.FactoryComponents.ReadJsonFile import ReadJsonFile as ReadJsonFile
from src.DevelopToolBox.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileFactory.FactoryComponents.ReadIniFile import ReadIniFile as ReadIniFile
from src.DevelopToolBox.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileFactory.FactoryComponents.Abstract import AbstractFactoryComponent


class ReadFileFactory(object):
    def __init__(self):
        self.logger = logging.getLogger('ConfigurationReader_logger')

    def get_file_reader(self, path: str, datatype: str) -> AbstractFactoryComponent:
        try:
            if datatype == "json":
                self.logger.debug(f"reader is ReadJsonFile")
                file_reader: AbstractFactoryComponent = ReadJsonFile(path)
            elif datatype == "ini":
                self.logger.debug(f"reader is ReadIniFile")
                file_reader: AbstractFactoryComponent = ReadIniFile(path)
            else:
                self.logger.critical(f"no such type of data_file {datatype}")
                exit(1)
            self.logger.debug(f"reader returned")
            return file_reader
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

