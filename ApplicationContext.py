#
#
#
import logging
import inspect

from Global2p2.InterfaceApplicationContext import InterfaceApplicationContext

from DomainService.DomainService import DomainService

from Global2p1.InterfaceDaoNodeUnit import InterfaceDaoNodeUnit
from DaoNodeUnit import DaoNodeUnit

# InterfaceNodeUnitRepository / InterfaceNodeUnitDescriptionRepository / InterfaceNodeUnitDescriptionIdRepository
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.InterfaceNodeUnitDescriptionRepository import InterfaceNodeUnitDescriptionRepository
from Global2p1.InterfaceNodeUnitDescriptionIdRepository import InterfaceNodeUnitDescriptionIdRepository
from NodeUnitRepository.NodeUnitRepository import NodeUnitRepository

from Global.InterfaceNodeUnitIterator import InterfaceNodeUnitIterator
from NodeUnitIterator.NodeUnitIterator import NodeUnitIterator

from Global.NodeUnitDescription import NodeUnitDescription

from Global.InterfaceModuleManager import InterfaceModuleManager
from WorkersManager.impl_WorkersManager import impl_WorkersManager

from Global2p2.i_WorkersRepository import i_WorkersRepository
from WorkersRepository.impl_WorkersRepository import impl_WorkersRepository

from Global2p2.i_DaoWorkers import i_DaoWorkers
from DaoWorkers.impl_DaoWorkers import impl_DaoWorkers

from Global2p2.i_DaoWorkersSpecifications import i_DaoWorkersSpecifications
from DaoWorkersSpecifications.impl_DaoWorkersSpecifications import impl_DaoWorkersSpecifications

from Global2p2.i_StorageManager import i_StorageManager
from StorageManager.impl_StorageManager import impl_StorageManager

from LibByzaticCommon import Exceptions
from typing import Optional


class ApplicationContext(InterfaceApplicationContext):
    __logger: Optional[logging.Logger] = None
    #
    __DomainService: Optional[DomainService] = None
    __RootNodeUnitDescription: Optional[NodeUnitDescription] = None
    #
    __WorkersRepository: Optional[i_WorkersRepository] = None
    __DaoWorkers: Optional[i_DaoWorkers] = None
    __DaoWorkersSpecifications: Optional[i_DaoWorkersSpecifications] = None
    #
    __ModuleManager: Optional[InterfaceModuleManager] = None
    __DaoNodeUnit: Optional[InterfaceDaoNodeUnit] = None
    __NodeUnitRepository: Optional[InterfaceNodeUnitRepository] = None
    __NodeUnitUnitDescriptionRepository: Optional[InterfaceNodeUnitDescriptionRepository] = None
    __NodeUnitIterator: Optional[InterfaceNodeUnitIterator] = None
    __StorageManager: Optional[i_StorageManager] = None

    def __getLogger(self) -> logging.Logger:
        try:
            if not self.__logger:
                self.__logger: logging.Logger = logging.getLogger("ApplicationContext-logger")
            return self.__logger
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    # TODO module_manager: InterfaceModuleManager for DomainService
    def getDomainService(self) -> DomainService:
        try:
            if not self.__DomainService:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__DomainService: DomainService = DomainService(self.getNodeUnitIterator(), self.getModuleManager())
            return self.__DomainService
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getDaoNodeUnit(self) -> InterfaceDaoNodeUnit:
        try:
            if not self.__DaoNodeUnit:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__DaoNodeUnit: InterfaceDaoNodeUnit = DaoNodeUnit("data/graph_data.json")
            return self.__DaoNodeUnit
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getModuleManager(self) -> InterfaceModuleManager:
        try:
            if not self.__ModuleManager:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__ModuleManager: InterfaceModuleManager = impl_WorkersManager(self.getNodeUnitRepository(), self.getWorkersRepository())
            return self.__ModuleManager
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getWorkersRepository(self) -> i_WorkersRepository:
        try:
            if not self.__WorkersRepository:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__WorkersRepository: i_WorkersRepository = impl_WorkersRepository(
                    dao_workers=self.getDaoWorkers(),
                    dao_workers_specifications=self.getDaoWorkersSpecifications(),
                    storage_manager=self.getStorageManager()
                )
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__WorkersRepository
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getStorageManager(self) -> i_StorageManager:
        try:
            if not self.__StorageManager:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__StorageManager: i_StorageManager = impl_StorageManager(
                    self.getNodeUnitRepository().get_root_node_unit().get_workers_pipeline().get_global_space().get_storages(),
                    self.getNodeUnitDescriptionRepository().get_all_node_unit_description()
                )
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__StorageManager
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getDaoWorkers(self) -> i_DaoWorkers:
        try:
            if not self.__DaoWorkers:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__DaoWorkers: i_DaoWorkers = impl_DaoWorkers()
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__DaoWorkers
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getDaoWorkersSpecifications(self) -> i_DaoWorkersSpecifications:
        try:
            if not self.__DaoWorkersSpecifications:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__DaoWorkersSpecifications: i_DaoWorkersSpecifications = impl_DaoWorkersSpecifications("data/modules_specification.json")
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__DaoWorkersSpecifications
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getNodeUnitRepository(self) -> InterfaceNodeUnitRepository:
        try:
            if not self.__NodeUnitRepository:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__NodeUnitRepository: InterfaceNodeUnitRepository = NodeUnitRepository(self.getDaoNodeUnit())
                self.__NodeUnitUnitDescriptionRepository = self.__NodeUnitRepository
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__NodeUnitRepository
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getNodeUnitDescriptionRepository(self) -> InterfaceNodeUnitDescriptionRepository:
        try:
            if not self.__NodeUnitUnitDescriptionRepository:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__NodeUnitUnitDescriptionRepository = NodeUnitRepository(self.getDaoNodeUnit())
                self.__NodeUnitRepository = self.__NodeUnitUnitDescriptionRepository
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__NodeUnitUnitDescriptionRepository
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getNodeUnitIterator(self) -> InterfaceNodeUnitIterator:
        try:
            if not self.__NodeUnitIterator:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__NodeUnitIterator: InterfaceNodeUnitIterator = NodeUnitIterator(self.getNodeUnitRepository(), self.getRootNodeUnitDescription())
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__NodeUnitIterator
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def getRootNodeUnitDescription(self) -> NodeUnitDescription:
        try:
            if not self.__RootNodeUnitDescription:
                self.__getLogger().debug(f"INITIALISATION OF {str(inspect.currentframe().f_code.co_name)}")
                self.__RootNodeUnitDescription = self.getNodeUnitRepository().get_root_node_unit_description()
            self.__getLogger().debug(f"RETURNING OF {str(inspect.currentframe().f_code.co_name)}")
            return self.__RootNodeUnitDescription
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setRootNodeDescription(self, instance_of: NodeUnitDescription):
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__RootNodeUnitDescription: NodeUnitDescription = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setDomainService(self, instance_of: DomainService) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__DomainService: DomainService = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setDaoNodeUnit(self, instance_of: InterfaceDaoNodeUnit) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__DaoNodeUnit: InterfaceDaoNodeUnit = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setNodeUnitRepository(self, instance_of: InterfaceNodeUnitRepository) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__NodeUnitRepository: InterfaceNodeUnitRepository = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setNodeUnitIterator(self, instance_of: InterfaceNodeUnitIterator) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__NodeUnitIterator: InterfaceNodeUnitIterator = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setRootNodeUnitDescription(self, instance_of: NodeUnitDescription) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__RootNodeUnitDescription: NodeUnitDescription = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setModuleManager(self, instance_of: InterfaceModuleManager) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__ModuleManager: InterfaceModuleManager = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setWorkersRepository(self, instance_of: i_WorkersRepository) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__WorkersRepository: i_WorkersRepository = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setStorageManager(self, instance_of: i_StorageManager):
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__StorageManager: i_StorageManager = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setDaoWorkers(self, instance_of: i_DaoWorkers) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__DaoWorkers: i_DaoWorkers = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def setDaoWorkersSpecifications(self, instance_of: i_DaoWorkersSpecifications) -> None:
        try:
            self.__getLogger().debug(f"SETTING OF {str(inspect.currentframe().f_code.co_name)}")
            self.__DaoWorkersSpecifications: i_DaoWorkersSpecifications = instance_of
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)
