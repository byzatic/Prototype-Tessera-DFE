#
#
#
import logging
from .ABCAbstractCollection import DaoPrometheusInterface
from .PrometheusQueryUnit import PrometheusQueryUnitInterface
from .PrometheusDto import i_DtoPrometheusMetric, i_DtoPrometheusMetricLabel
from .PrometheusDto import impl_DtoPrometheusMetric, impl_DtoPrometheusMetricLabel
from .QueryTransform import QueryTransformInterface, QueryTransform
from .PrometheusClient import PrometheusClientDtoInterface, PrometheusClientInterface, PrometheusClient
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from DaoPrometheus.LocalExceptions.BadDataException import BadDataException
from DaoPrometheus.LocalExceptions.ServerUnavailableException import ServerUnavailableException
from DaoPrometheus.DtoRawData.i_DtoRawData import i_DtoRawData
from DaoPrometheus.DtoRawData.impl_DtoRawData import impl_DtoRawData
from copy import deepcopy


class DaoPrometheus(DaoPrometheusInterface):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("Application-logger")
        self.__QueryTransform: QueryTransformInterface = QueryTransform()
        self.__PrometheusClient: PrometheusClientInterface = PrometheusClient()

    def get(self, prometheus_query_unit: PrometheusQueryUnitInterface) -> i_DtoPrometheusMetric:
        try:
            self.__logger.debug(f"Start getting data for: "
                                f"{prometheus_query_unit.queries_section_query_name}"
                                f" | "
                                f"{prometheus_query_unit.queries_section_id}")
            request_url: str = self.__QueryTransform.get_url(prometheus_query_unit)
            ssl_verify: bool = prometheus_query_unit.server_section_ssl_verify
            prometheus_raw_data: i_DtoRawData = self.__get_raw_data(request_url, ssl_verify)
            if prometheus_raw_data.getData() == {}:
                label_data_object: i_DtoPrometheusMetricLabel = impl_DtoPrometheusMetricLabel(
                    key="metrics_core_generated_reason",
                    sign="=",
                    value=f"MetricsCoreGenerated->{prometheus_raw_data.getStatus()}"
                )
                data_object: i_DtoPrometheusMetric = impl_DtoPrometheusMetric(
                    value=f"1",
                    metric_labels=[label_data_object],
                    timestamp=f""
                )
                return data_object
            else:
                fetched_data: str = self.__fetch_data(prometheus_raw_data)
                data_object: i_DtoPrometheusMetric = impl_DtoPrometheusMetric(
                    value=f"{fetched_data}",
                    timestamp=f"{prometheus_raw_data.getTs()}",
                    metric_labels=self.__fetch_labels(prometheus_raw_data)
                )
                return data_object
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __get_raw_data(self, request_url: str, ssl_verify: bool) -> i_DtoRawData:
        try:
            prometheus_client_dto: PrometheusClientDtoInterface = self.__PrometheusClient.get_by_url(
                request_url,
                ssl_verify
            )
            prometheus_raw_data: i_DtoRawData = impl_DtoRawData(
                data=prometheus_client_dto.data,
                status=prometheus_client_dto.status,
                ts=prometheus_client_dto.ts
            )
            prometheus_raw_data = self.__helper_bad_data_block_cleaner(prometheus_raw_data)
            return prometheus_raw_data
        except BadDataException as bde:
            self.__logger.warning(f"Can't get data because client returns BadDataException: {bde.args}")
            prometheus_raw_data: i_DtoRawData = impl_DtoRawData(
                data={},
                status="Bad Data Quality",
                ts=0
            )
            return prometheus_raw_data
        except ServerUnavailableException as sue:
            self.__logger.warning(f"Can't get data because client returns ServerUnavailableException: {sue.args}")
            prometheus_raw_data: i_DtoRawData = impl_DtoRawData(
                data={},
                status="Can't connect to server",
                ts=0
            )
            return prometheus_raw_data
        except OperationIncompleteException as oie:
            self.__logger.warning(f"Can't get data because client returns OperationIncompleteException: {oie.args}")
            prometheus_raw_data: i_DtoRawData = impl_DtoRawData(
                data={},
                status="Can't get data by undefined error",
                ts=0
            )
            return prometheus_raw_data
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __fetch_data(self, data: i_DtoRawData) -> str:
        try:
            self.__logger.debug(f"Start to fetch data")
            raw_data: dict = data.getData()
            raw_value_objects_list: list[dict] = raw_data["data"]["result"]
            max_raw_value_timestamp: float = 0.0
            max_raw_value_data: str = ''
            for raw_value in raw_value_objects_list:
                raw_value_list: list = raw_value["values"]
                for raw_value in raw_value_list:
                    raw_value_timestamp: int
                    raw_value_data: str
                    if isinstance(raw_value[0], float) or isinstance(raw_value[0], int):
                        raw_value_timestamp: float = float(raw_value[0])
                        raw_value_data: str = str(raw_value[1])
                    else:
                        raw_value_timestamp: float = float(raw_value[1])
                        raw_value_data: str = str(raw_value[0])
                    if raw_value_timestamp > max_raw_value_timestamp:
                        max_raw_value_timestamp = raw_value_timestamp
                        max_raw_value_data = raw_value_data
            self.__logger.debug(f"Finish to fetch data; Fetched data: {max_raw_value_data}")
            return max_raw_value_data
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __fetch_labels(self, data: i_DtoRawData) -> list[i_DtoPrometheusMetricLabel]:
        self.__logger.debug(f"try to fetch labels in {data.getData()}")
        label_data_object_list: list[i_DtoPrometheusMetricLabel] = []
        for key, value in data.getData()["data"]["result"][0]["metric"].items():
            label_data_object: i_DtoPrometheusMetricLabel = impl_DtoPrometheusMetricLabel(
                key=key,
                sign="=",
                value=value
            )
            label_data_object_list.append(label_data_object)
        self.__logger.debug(f"found {len(label_data_object_list)} label items")
        return label_data_object_list

    def __helper_bad_data_block_cleaner(self, prometheus_raw_data: i_DtoRawData) -> i_DtoRawData:
        deepcopy_of_prometheus_raw_data = deepcopy(prometheus_raw_data)
        raw_data = deepcopy_of_prometheus_raw_data.getData()
        list_raw_value: list = raw_data["data"]["result"]
        new_prometheus_raw_data: i_DtoRawData
        new_list_raw_value: list = []
        if len(list_raw_value) > 1:
            self.__logger.warning(f"found {len(list_raw_value)} raw value objects; nothing to do")
            for raw_value in list_raw_value:
                if raw_value["metric"] != {}:
                    new_list_raw_value.append(raw_value)
                else:
                    self.__logger.warning(f"found raw value object with empty metric field; removed")
            raw_data["data"]["result"] = new_list_raw_value
            new_prometheus_raw_data: i_DtoRawData = impl_DtoRawData(
                data=raw_data,
                status=deepcopy_of_prometheus_raw_data.getStatus(),
                ts=deepcopy_of_prometheus_raw_data.getTs()
            )
        else:
            new_prometheus_raw_data = deepcopy_of_prometheus_raw_data
        return new_prometheus_raw_data


