#
#
#
from abc import ABCMeta, abstractmethod
from src.LibByzaticCommon.Singleton import Singleton
from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.NodeUnit import NodeUnit


class InterfaceNodeUnitDescriptionIdRepository(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_node_unit_description_by_id(self, identification_name: str) -> NodeUnitDescription:
        pass

