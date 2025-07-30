#
#
#
import logging
from typing import Union
from DaoNodeUnit.LocalApi.InterfaceGraphDataReader import InterfaceGraphDataReader
from LibByzaticCommon.FileReaders import BaseReaderInterface, JsonFileReader
from LibByzaticCommon import Exceptions


class GraphDataReader(InterfaceGraphDataReader):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("DaoNodeUnit-logger")
        self.__JsonFileReader: BaseReaderInterface = JsonFileReader()

    def read_data(self, file_location: str) -> dict:
        try:
            data: Union[dict, list] = self.__JsonFileReader.read(file_location)
            if type(data) is list:
                Exceptions.OperationIncompleteException(
                    f"Incorrect graph data - root should be JSON object, not JSON array"
                )
            else:
                return data
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)
