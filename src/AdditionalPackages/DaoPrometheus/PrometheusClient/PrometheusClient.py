#
#
#
import calendar
import logging
from datetime import datetime as dt

from .ABCAbstractCollection import PrometheusClientInterface
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
import requests as promrequest
from requests import Response
from typing import Union
from .PrometheusClientDto import PrometheusClientDtoInterface, PrometheusClientDto
from DaoPrometheus.LocalExceptions.BadDataException import BadDataException
from DaoPrometheus.LocalExceptions.ServerUnavailableException import ServerUnavailableException


class PrometheusClient(PrometheusClientInterface):

    #https://demo1.askug.ru:443/api/monitoringprom/api/v1/query_range?query=%28metrics_core_installation%7Binstallation_name%3D%27DEMO%27%7D%29OR%20on%28%29%20vector%281%29&start=1696437003.040694&end=1696437543.040694&step=7

    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("Application-logger")

    def get_by_url(self, url: str, ssl_verify: bool) -> PrometheusClientDtoInterface:
        data: PrometheusClientDtoInterface = self.__http_s_get(url, ssl_verify, 10, True)
        return data

    def __http_s_get(self, url: str, ssl_verify: bool, server_get_timeout: int, automatic_retry_with_no_ssl: bool = True) -> PrometheusClientDtoInterface:
        try:
            self.__logger.debug(f"Starting HTTP(s) request")
            self.__logger.debug(f"HTTP(s) request parameter (url) request url: {type(url)} {url}")
            self.__logger.debug(f"HTTP(s) request parameter (server_get_timeout) request timeout: {type(server_get_timeout)} {server_get_timeout} sec.")
            self.__logger.debug(f"HTTP(s) request parameter (ssl_verify) SSL verification: {type(ssl_verify)} {ssl_verify}")

            self.__logger.debug(f"Running HTTP(s) request")
            response_raw: Response = promrequest.get(
                url=url,
                timeout=server_get_timeout,
                # TODO: There is a bug in ssl_verify from PrometheusQueryUnit: ssl_verify not always bool
                verify=bool(ssl_verify)
            )
            response_raw.close()
            self.__logger.debug(f"Server returns: {response_raw.content}")

            ts: int = int(dt.utcnow().strftime("%s"))
            self.__logger.debug(f"Current timestamp registered: {ts}")

            # Returns a number that indicates the HTTP response status
            self.__logger.debug(f"HTTP(s) server returns status code: {response_raw.status_code}")

            # Returns a text corresponding to the status code
            self.__logger.debug(f"Text corresponding to the status code: {response_raw.reason}")

            prometheus_client_dto: PrometheusClientDtoInterface = self.__make_processed_dto(response_raw, ts)

            return prometheus_client_dto

        except promrequest.exceptions.SSLError as erru:
            self.__logger.error(f"SSL Error: {erru}")
            self.__logger.error(f"Source URL: {url}")
            if ssl_verify and automatic_retry_with_no_ssl:
                self.__logger.warning(f"Retry with no SSL verify")
                response_data: PrometheusClientDtoInterface = self.__http_s_get(
                    url=url,
                    ssl_verify=False,
                    server_get_timeout=server_get_timeout
                )
                return response_data
            else:
                raise OperationIncompleteException(f"No SSL Request returns SSL error", errno=1)
        except promrequest.exceptions.Timeout as t:
            self.__logger.error(f"Timeout Error: {t}")
            self.__logger.error(f"Source URL: {url}")
            raise ServerUnavailableException(t.args, errno=t.errno)
        except promrequest.exceptions.ConnectionError as ce:
            self.__logger.error(f"Connection Error : {ce}")
            self.__logger.error(f"Source URL: {url}")
            raise ServerUnavailableException(ce.args, errno=ce.errno)
        except promrequest.exceptions.HTTPError as httpe:
            self.__logger.error(f"HTTP Error : {httpe}")
            self.__logger.error(f"Source URL: {url}")
            raise ServerUnavailableException(httpe.args, errno=httpe.errno)
        except promrequest.exceptions.RequestException as re:
            self.__logger.error(f"Request Error : {re}")
            self.__logger.error(f"Source URL: {url}")
            raise ServerUnavailableException(re.args, errno=re.errno)
        except promrequest.exceptions.JSONDecodeError as jde:
            self.__logger.error(f"Request Error : {jde}")
            self.__logger.error(f"Source URL: {url}")
            raise BadDataException(jde.args, errno=jde.errno)
        except OperationIncompleteException as oie:
            self.__logger.error(f"Operation Incomplete Error : {oie}")
            self.__logger.error(f"Source URL: {url}")
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __make_processed_dto(self, response_raw: Response, response_ts: int) -> PrometheusClientDtoInterface:

        response_data: Union[dict, list]
        response_satus: str

        response_data: Union[dict, list] = response_raw.json()
        self.__logger.debug(f"Response data: {response_data}")

        response_satus = self.__extract_prometheus_response_status(response_data)
        self.__logger.debug(f"Prometheus status is {response_satus}")

        prometheus_client_dto: PrometheusClientDtoInterface = PrometheusClientDto(
            data=response_data,
            status=response_satus,
            ts=response_ts
        )

        return prometheus_client_dto

    def __extract_prometheus_response_status(self, response_data: Union[dict, list]):
        if "status" in response_data:
            status: str = response_data["status"]
            self.__logger.debug(f"Status extracted: status -> {status}")
            return status
        else:
            raise BadDataException(f"Bad data, Can't extract status from data")

