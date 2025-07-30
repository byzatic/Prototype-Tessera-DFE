#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnit


class InterfaceGraphDataUnmarshaller(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def unmarshal(self, raw_data: dict) -> DtoRawGraphDataNodeUnit:
        pass
