#
#
#
from abc import ABCMeta, abstractmethod
from LibByzaticCommon.Singleton.Singleton import Singleton
# from DomainService.DomainService import DomainService
from Global2p1.InterfaceDaoNodeUnit import InterfaceDaoNodeUnit
# InterfaceNodeUnitRepository / InterfaceNodeUnitDescriptionRepository / InterfaceNodeUnitDescriptionIdRepository
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
# from Global.InterfaceNodeUnitIterator import InterfaceNodeUnitIterator
from Global.NodeUnitDescription import NodeUnitDescription
# from Global.InterfaceModuleManager import InterfaceModuleManager
# from Global2p2.i_WorkersRepository import i_WorkersRepository
# from Global2p2.i_DaoWorkers import i_DaoWorkers
# from Global2p2.i_DaoWorkersSpecifications import i_DaoWorkersSpecifications
from Global2p2.i_StorageManager import i_StorageManager


class i_WorkerContext(Singleton):
    __metaclass__ = ABCMeta

    # @abstractmethod
    # def getDomainService(self) -> DomainService:
    #     pass

    @abstractmethod
    def getDaoNodeUnit(self) -> InterfaceDaoNodeUnit:
        pass

    # @abstractmethod
    # def getModuleManager(self) -> InterfaceModuleManager:
    #     pass

    # @abstractmethod
    # def getWorkersRepository(self) -> i_WorkersRepository:
    #     pass

    @abstractmethod
    def getStorageManager(self) -> i_StorageManager:
        pass

    # @abstractmethod
    # def getDaoWorkers(self) -> i_DaoWorkers:
    #     pass

    # @abstractmethod
    # def getDaoWorkersSpecifications(self) -> i_DaoWorkersSpecifications:
    #     pass

    @abstractmethod
    def getNodeUnitRepository(self) -> InterfaceNodeUnitRepository:
        pass

    # @abstractmethod
    # def getNodeUnitIterator(self) -> InterfaceNodeUnitIterator:
    #     pass

    @abstractmethod
    def getRootNodeUnitDescription(self) -> NodeUnitDescription:
        pass
