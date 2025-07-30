#
#
#
import logging
from typing import Optional
from AdditionalPackages.DaoPrometheus.PrometheusQueryUnit import PrometheusQueryUnit
from AdditionalPackages.DaoPrometheus.PrometheusQueryUnit import PrometheusQueryLabel
from DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration.PrometheusQueryConfiguration import PrometheusQueryConfiguration
from LibByzaticCommon import Exceptions


class SupportConvertPrometheusQueryConfigurationToPrometheusQueryUnit(object):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("Workers-PrometheusGetData-logger")

    def convert(self, prometheus_query_configuration_unit: PrometheusQueryConfiguration, query_id: str) -> PrometheusQueryUnit:
        queries_section_query_name: Optional[str] = None
        queries_section_id: Optional[str] = None
        queries_section_upper_limit: Optional[str] = None
        queries_section_lower_limit: Optional[str] = None
        queries_section_step: Optional[str] = None
        queries_section_time_range: Optional[str] = None
        queries_section_labels: Optional[list[PrometheusQueryLabel]] = None

        for query_description in prometheus_query_configuration_unit.getQueryDescription():
            if query_description.getQueryId() == query_id:
                queries_section_id = query_description.getQueryId()
                queries_section_query_name = query_description.getQueryType()
                queries_section_upper_limit = query_description.getUpperLimit()
                queries_section_lower_limit = query_description.getLowerLimit()
                queries_section_step = query_description.getStep()
                queries_section_time_range = query_description.getTimeRange()
                queries_section_labels_list: list[PrometheusQueryLabel] = []
                for query_description_label in query_description.getLabels():
                    prometheus_query_label_unit: PrometheusQueryLabel = PrometheusQueryLabel(
                        label_value=query_description_label.getLabelValue(),
                        label_key=query_description_label.getLabelKey(),
                        label_sign=query_description_label.getLabelSign()
                    )
                    queries_section_labels_list.append(prometheus_query_label_unit)
                queries_section_labels = queries_section_labels_list

        if queries_section_query_name is None:
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfiguration -> PrometheusQueryUnit: query type not found")

        if queries_section_id is None:
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfiguration -> PrometheusQueryUnit: query id not found")

        if queries_section_upper_limit is None:
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfiguration -> PrometheusQueryUnit: upper limit not found")

        if queries_section_lower_limit is None:
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfiguration -> PrometheusQueryUnit: lower limit not found")

        if queries_section_step is None:
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfiguration -> PrometheusQueryUnit: step not found")

        if queries_section_time_range is None:
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfiguration -> PrometheusQueryUnit: time range not found")

        if queries_section_labels is None:
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfiguration -> PrometheusQueryUnit: query labels not found")

        prometheus_query_unit = PrometheusQueryUnit(
                                        server_section_url=prometheus_query_configuration_unit.getServerDescription().getUrl(),
                                        server_section_ssl_verify=bool(prometheus_query_configuration_unit.getServerDescription().getSslVerify()),
                                        queries_section_query_name=queries_section_query_name,
                                        queries_section_id=queries_section_id,
                                        queries_section_upper_limit=queries_section_upper_limit,
                                        queries_section_lower_limit=queries_section_lower_limit,
                                        queries_section_step=queries_section_step,
                                        queries_section_time_range=queries_section_time_range,
                                        queries_section_labels=queries_section_labels
                                        )
        return prometheus_query_unit






