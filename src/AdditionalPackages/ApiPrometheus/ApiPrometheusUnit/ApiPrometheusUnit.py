from dataclasses import dataclass
from .ApiPrometheusUnitLabel import ApiPrometheusUnitLabelInterface
from .ABCAbstractCollection import ApiPrometheusUnitInterface


@dataclass(frozen=True)
class ApiPrometheusUnit(ApiPrometheusUnitInterface):
    metric_name: str = None
    metric_value: str = None
    metric_labels: list[ApiPrometheusUnitLabelInterface] = None
