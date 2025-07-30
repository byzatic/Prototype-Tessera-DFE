#
#
#
from abc import ABCMeta, abstractmethod
from Global2p2.InterfaceApplicationContext import InterfaceApplicationContext


class i_ServicePrometheus(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run_service(self) -> None:
        pass
