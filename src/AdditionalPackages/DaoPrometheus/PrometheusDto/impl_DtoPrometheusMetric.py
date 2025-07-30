from dataclasses import dataclass
from .ABCAbstractCollection.i_DtoPrometheusMetric import i_DtoPrometheusMetric
from .ABCAbstractCollection.i_DtoPrometheusMetricLabel import i_DtoPrometheusMetricLabel


@dataclass(frozen=True)
class impl_DtoPrometheusMetric(i_DtoPrometheusMetric):
    value: str = None
    timestamp: str = None
    metric_labels: list[i_DtoPrometheusMetricLabel] = None
