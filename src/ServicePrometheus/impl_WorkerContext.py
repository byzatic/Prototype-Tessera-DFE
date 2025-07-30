#
#
#
import logging
from typing import Optional
from ServicePrometheus.i_WorkerContext import i_WorkerContext
from LibByzaticCommon import Exceptions

# from DomainService.DomainService import DomainService

# from Global.InterfaceNodeUnitIterator import InterfaceNodeUnitIterator
from Global.NodeUnitDescription import NodeUnitDescription
# from Global.InterfaceModuleManager import InterfaceModuleManager

from Global2p1.InterfaceDaoNodeUnit import InterfaceDaoNodeUnit
# InterfaceNodeUnitRepository / InterfaceNodeUnitDescriptionRepository / InterfaceNodeUnitDescriptionIdRepository
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository

# from Global2p2.i_WorkersRepository import i_WorkersRepository
from Global2p2.InterfaceApplicationContext import InterfaceApplicationContext
# from Global2p2.i_DaoWorkers import i_DaoWorkers
# from Global2p2.i_DaoWorkersSpecifications import i_DaoWorkersSpecifications
from Global2p2.i_StorageManager import i_StorageManager


class impl_WorkerContext(i_WorkerContext):
    #
    # __DomainService: Optional[DomainService] = None
    __RootNodeUnitDescription: Optional[NodeUnitDescription] = None
    #
    # __WorkersRepository: Optional[i_WorkersRepository] = None
    # __DaoWorkers: Optional[i_DaoWorkers] = None
    # __DaoWorkersSpecifications: Optional[i_DaoWorkersSpecifications] = None
    #
    # __ModuleManager: Optional[InterfaceModuleManager] = None
    __DaoNodeUnit: Optional[InterfaceDaoNodeUnit] = None
    __NodeUnitRepository: Optional[InterfaceNodeUnitRepository] = None
    # __NodeUnitIterator: Optional[InterfaceNodeUnitIterator] = None
    __StorageManager: Optional[i_StorageManager] = None

    def __init__(self, application_context: Optional[InterfaceApplicationContext] = None):
        self.__logger: logging.Logger = logging.getLogger("WorkerContext-logger")
        try:
            if application_context is None:
                raise Exceptions.OperationIncompleteException(f"To initialise a WorkerContext for the first time, "
                                                              f"you need to pass an object InterfaceApplicationContext there.")
            #
            # self.__DomainService: Optional[DomainService] = application_context.getDomainService()
            self.__RootNodeUnitDescription: Optional[NodeUnitDescription] = application_context.getRootNodeUnitDescription()
            #
            # self.__WorkersRepository: Optional[i_WorkersRepository] = application_context.getWorkersRepository()
            # self.__DaoWorkers: Optional[i_DaoWorkers] = application_context.getDaoWorkers()
            # self.__DaoWorkersSpecifications: Optional[i_DaoWorkersSpecifications] = application_context.getDaoWorkersSpecifications()
            #
            # self.__ModuleManager: Optional[InterfaceModuleManager] = application_context.getModuleManager()
            self.__DaoNodeUnit: Optional[InterfaceDaoNodeUnit] = application_context.getDaoNodeUnit()
            self.__NodeUnitRepository: Optional[InterfaceNodeUnitRepository] = application_context.getNodeUnitRepository()
            # self.__NodeUnitIterator: Optional[InterfaceNodeUnitIterator] = application_context.getNodeUnitIterator()
            self.__StorageManager: Optional[i_StorageManager] = application_context.getStorageManager()
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    # def getDomainService(self) -> DomainService:
    #     return self.__DomainService

    def getDaoNodeUnit(self) -> InterfaceDaoNodeUnit:
        return self.__DaoNodeUnit

    # def getModuleManager(self) -> InterfaceModuleManager:
    #     return self.__ModuleManager
    #
    # def getWorkersRepository(self) -> i_WorkersRepository:
    #     return self.__WorkersRepository

    def getStorageManager(self) -> i_StorageManager:
        return self.__StorageManager

    # def getDaoWorkers(self) -> i_DaoWorkers:
    #     return self.__DaoWorkers
    #
    # def getDaoWorkersSpecifications(self) -> i_DaoWorkersSpecifications:
    #     return self.__DaoWorkersSpecifications

    def getNodeUnitRepository(self) -> InterfaceNodeUnitRepository:
        return self.__NodeUnitRepository

    # def getNodeUnitIterator(self) -> InterfaceNodeUnitIterator:
    #     return self.__NodeUnitIterator

    def getRootNodeUnitDescription(self) -> NodeUnitDescription:
        return self.__RootNodeUnitDescription
