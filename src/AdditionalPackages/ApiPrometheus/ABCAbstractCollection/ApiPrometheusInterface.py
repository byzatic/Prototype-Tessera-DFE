#
#
#

from abc import ABCMeta, abstractmethod
from multiprocessing import Process
from ..ApiPrometheusUnit import ApiPrometheusUnitInterface
from src.LibByzaticCommon.Singleton import Singleton


class ApiPrometheusInterface(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, host: str = "0.0.0.0", port: str = "8080", location: str = "/metrics"):
        pass

    @abstractmethod
    def run_api(self) -> Process:
        pass

    @abstractmethod
    def publish(self, api_prometheus_unit_list: list[ApiPrometheusUnitInterface]) -> None:
        pass

    @abstractmethod
    def revive(self) -> None:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass

    @abstractmethod
    def is_alive_with_exception(self) -> None:
        pass

    @abstractmethod
    def terminate(self):
        pass
