from abc import ABCMeta, abstractmethod
from typing import Optional
from src.AdditionalPackages.DaoPrometheus.PrometheusQueryTemplateUnitRepository.PrometheusQueryTemplateUnit import PrometheusQueryTemplateUnitInterface


class PrometheusQueryTemplateUnitRepositoryInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self) -> None:
        pass

    def get(self, query_name: Optional[str] = None) -> PrometheusQueryTemplateUnitInterface:
        pass

    def get_list_all_available_query_template_unit(self) -> list[PrometheusQueryTemplateUnitInterface]:
        pass