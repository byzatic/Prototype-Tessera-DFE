from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class i_DtoPrometheusMetricLabel():
    __metaclass__ = ABCMeta

    def __init__(self,
                 key: str = None,
                 sign: str = None,
                 value: str = None
                 ) -> None:
        pass

    key: str = None
    sign: str = None
    value: str = None
