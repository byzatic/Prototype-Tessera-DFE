from dataclasses import dataclass
from .ABCAbstractCollection import ApiPrometheusUnitLabelInterface


@dataclass(frozen=True)
class ApiPrometheusUnitLabel(ApiPrometheusUnitLabelInterface):
    label_value: str = None
    label_key: str = None
    label_sign: str = None

