from .ABCAbstractCollection import PrometheusQueryTemplateUnitInterface
from dataclasses import dataclass


@dataclass(frozen=True)
class PrometheusQueryTemplateUnit(PrometheusQueryTemplateUnitInterface):
    query_name: str = None
    query_template: str = None
