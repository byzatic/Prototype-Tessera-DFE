#
# ImportModulesFactoryInterface
#

#
#
#
from abc import ABCMeta, abstractmethod
from types import ModuleType
from src.LibByzaticCommon.Singleton.Singleton import Singleton


class ImportModulesFactoryInterface(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fabricate(self, relative_name: str, root_package=False, relative_globals=None, level=0) -> ModuleType:
        pass
