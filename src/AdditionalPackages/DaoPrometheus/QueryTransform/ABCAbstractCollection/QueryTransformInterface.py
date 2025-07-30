from abc import ABCMeta, abstractmethod
from src.AdditionalPackages.DaoPrometheus.PrometheusQueryUnit import PrometheusQueryUnitInterface


class QueryTransformInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_url(self, prometheus_query_unit: PrometheusQueryUnitInterface) -> str:
        pass
