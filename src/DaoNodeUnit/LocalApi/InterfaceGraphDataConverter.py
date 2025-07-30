#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnit
from DaoNodeUnit.NodeUnitStorage.DtoNodeUnitStorage import DtoNodeUnitStorage


class InterfaceGraphDataConverter(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert(self, dto_node_unit: DtoRawGraphDataNodeUnit) -> DtoNodeUnitStorage:
        pass

