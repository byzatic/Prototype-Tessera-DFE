#
#
#
import logging
from typing import Union, Dict, List
import yaml
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from src.LibByzaticCommon.FileReaders.ABCAbstractCollection.BaseReaderInterface import BaseReaderInterface


class YamlFileReader(BaseReaderInterface):
    def __init__(self):
        self.logger = logging.getLogger("LibByzaticCommon-FileReaders-logger")

    def read(self, path: str) -> Union[Dict, List]:
        """
        read YAML file to Dict or List
        @param path: path to file
        @return: Dict or List if success or raise OperationIncompleteException from LibByzaticCommon.Exceptions
        """
        try:
            with open(path, "r") as file:
                """
                Another option offered by Python is to use a "with" statement which will ensure 
                the file is closed when the code that uses it finishes running. 
                This holds true even if an exception is thrown.
                """
                data: Union[Dict, List] = yaml.safe_load(file.read())
                self.logger.debug(f"YAML data is {data}")
                return data
        except FileNotFoundError as fnfe:
            raise OperationIncompleteException(fnfe.args, errno=fnfe.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)
