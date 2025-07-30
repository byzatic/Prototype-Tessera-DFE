from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from src.AdditionalPackages.DaoPrometheus.PrometheusQueryUnit.PrometheusQueryLabel import PrometheusQueryLabelInterface


@dataclass(frozen=True)
class PrometheusQueryUnitInterface():
    __metaclass__ = ABCMeta

    def __init__(self,
                 server_section_url: str = None,
                 server_section_ssl_verify: bool = None,
                 queries_section_query_name: str = None,
                 queries_section_id: str = None,
                 queries_section_upper_limit: str = None,
                 queries_section_lower_limit: str = None,
                 queries_section_step: str = None,
                 queries_section_time_range: str = None,
                 queries_section_labels: list[PrometheusQueryLabelInterface] = None
                 ) -> None:
        pass

    server_section_url: str = None
    server_section_ssl_verify: bool = None

    queries_section_query_name: str = None
    queries_section_id: str = None
    queries_section_upper_limit: str = None
    queries_section_lower_limit: str = None
    queries_section_step: str = None
    queries_section_time_range: str = None
    queries_section_labels: list[PrometheusQueryLabelInterface] = None
