from .ABCAbstractCollection.i_DtoPrometheusMetricLabel import i_DtoPrometheusMetricLabel
from dataclasses import dataclass


@dataclass(frozen=True)
class impl_DtoPrometheusMetricLabel(i_DtoPrometheusMetricLabel):
    key: str = None
    sign: str = None
    value: str = None
