from dataclasses import dataclass
from AdditionalPackages.DaoPrometheus.PrometheusQueryUnit.PrometheusQueryLabel import PrometheusQueryLabelInterface
from .ABCAbstractCollection import PrometheusQueryUnitInterface


@dataclass(frozen=True)
class PrometheusQueryUnit(PrometheusQueryUnitInterface):
    server_section_url: str = None
    server_section_ssl_verify: bool = None

    queries_section_query_name: str = None
    queries_section_id: str = None
    queries_section_upper_limit: str = None
    queries_section_lower_limit: str = None
    queries_section_step: str = None
    queries_section_time_range: str = None
    queries_section_labels: list[PrometheusQueryLabelInterface] = None
