from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class PrometheusClientDtoInterface(object):
    __metaclass__ = ABCMeta

    def __init__(self,
                 data: Union[dict, list] = None,
                 status: str = None,
                 ts: int = None
                 ) -> None:
        pass

    data: Union[dict, list] = None
    status: str = None
    # Unix Timestamp
    ts: int = None
