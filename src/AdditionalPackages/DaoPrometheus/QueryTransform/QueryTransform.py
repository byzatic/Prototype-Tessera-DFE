#
#
#
import logging
import urllib.parse as url_encode
from datetime import datetime, timedelta, timezone

from .ABCAbstractCollection import QueryTransformInterface

from ..PrometheusQueryTemplateUnitRepository import (PrometheusQueryTemplateUnitInterface,
                                                     PrometheusQueryTemplateUnitRepository,
                                                     PrometheusQueryTemplateUnitRepositoryInterface)
from src.AdditionalPackages.DaoPrometheus.PrometheusQueryUnit import PrometheusQueryUnitInterface, PrometheusQueryLabelInterface


class QueryTransform(QueryTransformInterface):
    # https://demo1.askug.ru:443/api/monitoringprom/api/v1/query_range?query=%28metrics_core_installation%7Binstallation_name%3D%27DEMO%27%7D%29OR%20on%28%29%20vector%281%29&start=1696437003.040694&end=1696437543.040694&step=7

    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("Application-logger")
        self.__PrometheusQueryTemplateUnitRepository: PrometheusQueryTemplateUnitRepositoryInterface = PrometheusQueryTemplateUnitRepository()

    def get_url(self, prometheus_query_unit: PrometheusQueryUnitInterface) -> str:
        url: str = self.__transform_prometheus_query_unit_to_url(prometheus_query_unit)
        return url

    def __transform_prometheus_query_unit_to_url(self, prometheus_query_unit: PrometheusQueryUnitInterface) -> str:

        time_delta: int = int(prometheus_query_unit.queries_section_time_range)
        time_start, time_stop = self.__get_times(time_delta)

        label_string: str = self.__generate_label_str(prometheus_query_unit.queries_section_labels)
        promql_query_template: str = self.__get_promql_query_template(prometheus_query_unit)
        promql_query: str = self.__modify_prometheus_query(
            promql_query_template,
            label_string,
            prometheus_query_unit.queries_section_upper_limit,
            prometheus_query_unit.queries_section_lower_limit
        )
        promql_query_quoted: str = self.__quote(promql_query)

        source_url: str = (f"{prometheus_query_unit.server_section_url}api/v1/query_range?query="
                           f"{promql_query_quoted}"
                           f"&start={time_start}&end={time_stop}"
                           f"&step={prometheus_query_unit.queries_section_step}")
        return source_url

    def __quote(self, data: str) -> str:
        """
        Each part of a URL, e.g. the path info, the query, etc.,
        has a different set of reserved characters that must be quoted. \n
        The quote function offers a cautious (not minimal) way to quote a string for most of these parts. \n
        :param data: str data to quote
        :return: quoted str data
        """
        quoted_data: str = url_encode.quote(data)
        return quoted_data

    # TODO: OLD FUNC
    def __get_times(self, delta: int) -> tuple[str, str]:
        time_now = datetime.now(tz=timezone.utc)
        time_start = str(datetime.timestamp(time_now - timedelta(minutes=delta)))
        time_stop = str(datetime.timestamp(time_now))
        return time_start, time_stop

    def __modify_prometheus_query(self, promql_query: str, label_str: str, h_limit: str, l_limit: str):
        promql_query = promql_query.replace('HLIMITPLACEHOLDER', h_limit)
        promql_query = promql_query.replace('LLIMITPLACEHOLDER', l_limit)
        promql_query = promql_query.replace('TAGLINEPLACEHOLDER', label_str)
        self.__logger.debug(f"Modifying query template complete: {str(promql_query)}")
        return promql_query

    def __generate_label_str(self, queries_section_labels: list[PrometheusQueryLabelInterface]):
        label_str: str = ""
        label_list: list[str] = self.__generate_label_list(queries_section_labels)
        for label in label_list:
            label_str = f"{label},{label_str}"
        label_str = "{" + label_str
        size = len(label_str)
        # replace last char with this
        replacement = "}"
        label_str = label_str[:-1] + replacement
        return label_str

    def __generate_label_list(self, queries_section_labels: list[PrometheusQueryLabelInterface]) -> list[str]:
        label_list: list[str] = []
        for prometheus_query_label in queries_section_labels:
            label: str = (f"{prometheus_query_label.label_key} "
                          f"{prometheus_query_label.label_sign} "
                          f"'{prometheus_query_label.label_value}'")
            label_list.append(label)
        return label_list

    def __get_promql_query_template(self, prometheus_query_unit: PrometheusQueryUnitInterface) -> str:
        prometheus_query_template_unit: PrometheusQueryTemplateUnitInterface = self.__PrometheusQueryTemplateUnitRepository.get(prometheus_query_unit.queries_section_query_name)
        query_template: str = prometheus_query_template_unit.query_template
        return query_template
