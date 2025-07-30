from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from src.LibByzaticCommon.Singleton import Singleton


@dataclass(frozen=True)
class ApiPrometheusControllerInterface(Singleton):
    __metaclass__ = ABCMeta

    def __init__(self,
                 metric_name: str = None,
                 metric_value: str = None,
                 ) -> None:
        pass

    metric_name: str = None
    metric_value: str = None
