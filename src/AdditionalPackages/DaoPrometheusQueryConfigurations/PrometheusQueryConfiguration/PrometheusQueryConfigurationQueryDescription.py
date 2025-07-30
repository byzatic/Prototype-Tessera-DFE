#
#
#
from .PrometheusQueryConfigurationQueryDescriptionLabels import PrometheusQueryConfigurationQueryDescriptionLabels


class PrometheusQueryConfigurationQueryDescription(object):
    def __init__(self, query_id: str, query_type: str, upper_limit: str, lower_limit: str, step: str, time_range: str, labels: list[PrometheusQueryConfigurationQueryDescriptionLabels]):
        self.__query_id: str = query_id
        self.__query_type: str = query_type
        self.__upper_limit: str = upper_limit
        self.__lower_limit: str = lower_limit
        self.__step: str = step
        self.__time_range: str = time_range
        self.__labels: list[PrometheusQueryConfigurationQueryDescriptionLabels] = labels

    def getQueryId(self) -> str:
        return self.__query_id

    def getQueryType(self) -> str:
        return self.__query_type

    def getUpperLimit(self) -> str:
        return self.__upper_limit

    def getLowerLimit(self) -> str:
        return self.__lower_limit

    def getStep(self) -> str:
        return self.__step

    def getTimeRange(self) -> str:
        return self.__time_range

    def getLabels(self) -> list[PrometheusQueryConfigurationQueryDescriptionLabels]:
        return self.__labels
