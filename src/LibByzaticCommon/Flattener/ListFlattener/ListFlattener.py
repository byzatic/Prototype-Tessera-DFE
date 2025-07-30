#
#
#
import logging
from src.LibByzaticCommon.Flattener.DLFlattener.DLFlattener import DLFlattener
from src.LibByzaticCommon.Flattener.Abstract import AbstractListFlattener


class ListFlattener(AbstractListFlattener):
    def __init__(self):
        self.logger = logging.getLogger("app")
        self.__flattener: DLFlattener = DLFlattener()

    def flatten(self, data_object: list, separator: str = '.') -> dict:
        """
        Turn a nested dictionary into a flattened dictionary
        :param_name data_object: The list to flatten
        :param_name separator: The string used to separate flattened keys
        :return: A flattened dictionary
        """
        flatten_dict: dict = self.__flattener.flatten(data_object, separator)
        return flatten_dict
