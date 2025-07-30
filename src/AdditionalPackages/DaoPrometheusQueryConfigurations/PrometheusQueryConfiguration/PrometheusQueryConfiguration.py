#
#
from .PrometheusQueryConfigurationServerDescription import PrometheusQueryConfigurationServerDescription
from .PrometheusQueryConfigurationQueryDescription import PrometheusQueryConfigurationQueryDescription


class PrometheusQueryConfiguration(object):
    def __init__(self, server_description: PrometheusQueryConfigurationServerDescription, query_description: list[PrometheusQueryConfigurationQueryDescription]):
        self.__server_description: PrometheusQueryConfigurationServerDescription = server_description
        self.__query_description: list[PrometheusQueryConfigurationQueryDescription] = query_description

    def getServerDescription(self) -> PrometheusQueryConfigurationServerDescription:
        return self.__server_description

    def getQueryDescription(self) -> list[PrometheusQueryConfigurationQueryDescription]:
        return self.__query_description
