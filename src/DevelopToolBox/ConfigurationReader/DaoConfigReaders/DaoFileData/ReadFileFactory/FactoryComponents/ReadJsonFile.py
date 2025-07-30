#
#
#
import logging
from typing import Union, Dict, List
from src.DevelopToolBox.ConfigurationReader.DaoConfigReaders.DaoFileData.ReadFileFactory.FactoryComponents.Abstract import AbstractFactoryComponent
from src.LibByzaticCommon.Flattener.JsonFlattener.JsonFlattener import JsonFlattener
from src.LibByzaticCommon.FileReaders.JsonFileReader import JsonFileReader as JsonFileReader
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ReadJsonFile(AbstractFactoryComponent):
    def __init__(self, path: str):
        self.logger = logging.getLogger("ConfigurationReader_logger")
        self.__path: str = path
        self.__json_file_reader = JsonFileReader()
        self.__json_flattener = JsonFlattener()

    def read(self) -> dict:
        try:
            json_object: Union[Dict, List] = self.__json_file_reader.read(self.__path)
            flatten_json_object = self.__reade_worker(json_object)
            return flatten_json_object
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __flatten_object_normaliser(self, flatten_object: dict) -> dict:
        normalised_flatten_object: dict = {}
        for flatten_key, flatten_value in flatten_object.items():
            new_flatten_key = flatten_key.replace('0.', '', 1)
            if new_flatten_key not in normalised_flatten_object:
                normalised_flatten_object[new_flatten_key] = flatten_value
            else:
                raise OperationIncompleteException(f"can't normalise {flatten_object}, key duplication by {new_flatten_key}")
        self.logger.debug(f"Flatten object normalised")
        return normalised_flatten_object

    def __reade_worker(self, json_object: Union[Dict, List]) -> dict:
        data: dict
        if isinstance(json_object, list):
            data = self.__isinstance_list(json_object)
        elif isinstance(json_object, dict):
            data = self.__isinstance_dict(json_object)
        else:
            raise OperationIncompleteException("Json reader internal error; loaded object have incorrect type")
        return data

    def __isinstance_list(self, list_object: list) -> dict:
        self.logger.warning(f"json loaded is list; you use one json object in list; "
                            f"better use json object without list")
        self.logger.debug(f"list_object {type(list_object)}: {list_object}")
        if len(list_object) > 1:
            raise OperationIncompleteException("Unsupported data object; json loaded list contains more then one json object")
        flatten_json_object: dict = self.__json_flattener.flatten(list_object)
        normalised_flatten_json_object: dict = self.__flatten_object_normaliser(flatten_json_object)
        return normalised_flatten_json_object

    def __isinstance_dict(self, dict_object) -> dict:
        self.logger.debug(f"json loaded is dict")
        flatten_json_object = self.__json_flattener.flatten(dict_object)
        return flatten_json_object
