from abc import ABCMeta, abstractmethod
from src.AdditionalPackages.DaoPrometheus.PrometheusQueryUnit import PrometheusQueryUnitInterface
from src.AdditionalPackages.DaoPrometheus.PrometheusDto import i_DtoPrometheusMetric


class DaoPrometheusInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get(self, prometheus_query_unit: PrometheusQueryUnitInterface) -> i_DtoPrometheusMetric:
        pass
