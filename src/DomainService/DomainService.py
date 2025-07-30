#
#
#
import logging
from Global.InterfaceNodeUnitIterator import InterfaceNodeUnitIterator
from Global.NodeUnitDescription import NodeUnitDescription
from Global.InterfaceModuleManager import InterfaceModuleManager
from src.LibByzaticCommon import Exceptions


class DomainService(object):
    __NodeUnitIterator: InterfaceNodeUnitIterator
    __ModuleManager: InterfaceModuleManager

    def __init__(self, iterator: InterfaceNodeUnitIterator, module_manager: InterfaceModuleManager):
        self.__logger: logging.Logger = logging.getLogger("DomainService-logger")
        self.__NodeUnitIterator: InterfaceNodeUnitIterator = iterator
        self.__ModuleManager: InterfaceModuleManager = module_manager

    def process(self) -> None:
        try:
            while self.__NodeUnitIterator.has_next():
                node_unit_description: NodeUnitDescription = self.__NodeUnitIterator.get_next()
                self.__ModuleManager.process_pipline(node_unit_description)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)
