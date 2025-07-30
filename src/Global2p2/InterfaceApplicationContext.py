#
#
#
from abc import ABCMeta, abstractmethod

from LibByzaticCommon.Singleton import Singleton

import logging

from DomainService.DomainService import DomainService

from Global2p1.InterfaceDaoNodeUnit import InterfaceDaoNodeUnit

from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.InterfaceNodeUnitDescriptionRepository import InterfaceNodeUnitDescriptionRepository
from Global2p1.InterfaceNodeUnitDescriptionIdRepository import InterfaceNodeUnitDescriptionIdRepository

from Global.InterfaceNodeUnitIterator import InterfaceNodeUnitIterator

from Global.NodeUnitDescription import NodeUnitDescription

from Global.InterfaceModuleManager import InterfaceModuleManager

from Global2p2.i_WorkersRepository import i_WorkersRepository

from Global2p2.i_DaoWorkers import i_DaoWorkers

from Global2p2.i_DaoWorkersSpecifications import i_DaoWorkersSpecifications
from Global2p2.i_StorageManager import i_StorageManager


class InterfaceApplicationContext(Singleton):
    __metaclass__ = ABCMeta

    __logger: logging.Logger
    #
    __DomainService: DomainService
    __RootNodeUnitDescription: NodeUnitDescription
    #
    __WorkersRepository: i_WorkersRepository
    __DaoWorkers: i_DaoWorkers
    __DaoWorkersSpecifications: i_DaoWorkersSpecifications
    #
    __ModuleManager: InterfaceModuleManager
    __DaoNodeUnit: InterfaceDaoNodeUnit
    __NodeUnitRepository: InterfaceNodeUnitRepository
    __NodeUnitIterator: InterfaceNodeUnitIterator
    __StorageManager: i_StorageManager

    @abstractmethod
    def __getLogger(self) -> logging.Logger:
        pass

    @abstractmethod
    def getDomainService(self) -> DomainService:
        pass

    @abstractmethod
    def getModuleManager(self) -> InterfaceModuleManager:
        pass

    @abstractmethod
    def getWorkersRepository(self) -> i_WorkersRepository:
        pass

    @abstractmethod
    def getDaoWorkers(self) -> i_DaoWorkers:
        pass

    @abstractmethod
    def getDaoWorkersSpecifications(self) -> i_DaoWorkersSpecifications:
        pass

    @abstractmethod
    def getDaoNodeUnit(self) -> InterfaceDaoNodeUnit:
        pass

    @abstractmethod
    def getNodeUnitRepository(self) -> InterfaceNodeUnitRepository:
        pass

    @abstractmethod
    def getNodeUnitIterator(self) -> InterfaceNodeUnitIterator:
        pass

    @abstractmethod
    def getRootNodeUnitDescription(self) -> NodeUnitDescription:
        pass

    @abstractmethod
    def setRootNodeDescription(self, instance_of: NodeUnitDescription):
        pass

    @abstractmethod
    def setDomainService(self, instance_of: DomainService) -> None:
        pass

    @abstractmethod
    def setDaoNodeUnit(self, instance_of: InterfaceDaoNodeUnit) -> None:
        pass

    @abstractmethod
    def setNodeUnitRepository(self, instance_of: InterfaceNodeUnitRepository) -> None:
        pass

    @abstractmethod
    def setNodeUnitIterator(self, instance_of: InterfaceNodeUnitIterator) -> None:
        pass

    @abstractmethod
    def setRootNodeUnitDescription(self, instance_of: NodeUnitDescription) -> None:
        pass

    @abstractmethod
    def setModuleManager(self, instance_of: InterfaceModuleManager) -> None:
        pass

    @abstractmethod
    def setWorkersRepository(self, instance_of: i_WorkersRepository) -> None:
        pass

    @abstractmethod
    def getStorageManager(self) -> i_StorageManager:
        pass

    @abstractmethod
    def setStorageManager(self, instance_of: i_StorageManager) -> None:
        pass

    @abstractmethod
    def setDaoWorkers(self, instance_of: i_DaoWorkers) -> None:
        pass

    @abstractmethod
    def setDaoWorkersSpecifications(self, instance_of: i_DaoWorkersSpecifications) -> None:
        pass
