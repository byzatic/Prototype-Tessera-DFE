#
#
#
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser


class AbstractFlattener():
    metaclass = ABCMeta

    @abstractmethod
    def flatten(self, data: any, separator: str = '.') -> dict:
        pass


class AbstractDictionaryFlattener(AbstractFlattener):
    metaclass = ABCMeta

    @abstractmethod
    def flatten(self, data: dict, separator: str = '.') -> dict:
        pass


class AbstractListFlattener(AbstractFlattener):
    metaclass = ABCMeta

    @abstractmethod
    def flatten(self, data: list, separator: str = '.') -> dict:
        pass


class AbstractJsonFlattener(AbstractFlattener):
    metaclass = ABCMeta

    @abstractmethod
    def flatten(self, data: list or dict, separator: str = '.') -> dict:
        pass


class AbstractConfigParserFlattener(AbstractFlattener):
    metaclass = ABCMeta

    @abstractmethod
    def flatten(self, data: ConfigParser, separator: str = '.') -> dict:
        pass


class AbstractDLFlattener(AbstractFlattener):
    metaclass = ABCMeta

    @abstractmethod
    def flatten(self, data: dict or list, separator: str = '.') -> dict:
        pass
