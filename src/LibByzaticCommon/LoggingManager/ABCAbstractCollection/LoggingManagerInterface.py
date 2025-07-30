#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton.Singleton import Singleton


class LoggingManagerInterface(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_logging(self, configuration_file: str, configuration_type: str, configuration_dict: dict = None) -> None:
        pass
