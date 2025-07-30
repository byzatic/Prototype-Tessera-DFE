#
#
#
import logging
from src.LibByzaticCommon.ImportModulesFactory import ImportModulesFactoryInterface
from src.LibByzaticCommon.ImportModulesFactory import ImportModulesFactory
from Global2p2.i_DaoWorkers import i_DaoWorkers
from Global2p2.i_Worker import i_Worker
from Global2p2.WorkerSpecification.WorkerSpecification import WorkerSpecification
from typing import Union
from types import ModuleType
from LibByzaticCommon import Exceptions


class impl_DaoWorkers(i_DaoWorkers):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("DaoWorkers-logger")
        self.__ImportModulesFactory: ImportModulesFactoryInterface = ImportModulesFactory()

    def get_worker(self, specification: WorkerSpecification) -> i_Worker:
        try:
            module: Union[ModuleType, i_Worker] = self.__ImportModulesFactory.fabricate(specification.get_module_main_path())
            return module
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)
