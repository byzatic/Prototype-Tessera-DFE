from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class PrometheusQueryTemplateUnitInterface(object):
    __metaclass__ = ABCMeta

    def __init__(self,
                 query_name: str = None,
                 query_template: str = None
                 ) -> None:
        pass

    query_name: str = None
    query_template: str = None
