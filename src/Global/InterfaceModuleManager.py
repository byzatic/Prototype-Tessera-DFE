#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository


class InterfaceModuleManager(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_pipline(self, node_unit_description: NodeUnitDescription) -> None:
        pass

