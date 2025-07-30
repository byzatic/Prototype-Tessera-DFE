#!/usr/bin/env python3
#
# POPPY PROMETHEUS API
# version "1.0.0"
#

import logging
from typing import Union
from .ABCAbstractCollection import ApiPrometheusInterface
from multiprocessing import Process, Queue
from .ApiCore import ApiCoreInterface, ApiCore
from .ApiPrometheusUnit import ApiPrometheusUnitInterface
from .ApiPrometheusPublisher import ApiPrometheusPublisher, ApiPrometheusPublisherInterface
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ApiPrometheus(ApiPrometheusInterface):
    def __init__(self, host: str = "0.0.0.0", port: str = "8080", location: str = "/metrics", buffer_cleaning_interval: int = 30):
        self.__logger: logging.Logger = logging.getLogger("ApiPrometheus-logger")
        self.__version: str = "0.2.1"
        self.__host: str = host
        self.__port: str = port
        self.__location: str = location
        self.__buffer_cleaning_interval: int = buffer_cleaning_interval
        self.__queue_data_bridge = Queue()
        self.__ApiPrometheusPublisher: ApiPrometheusPublisherInterface = ApiPrometheusPublisher(self.__queue_data_bridge)
        self.__api_prometheus_process: Union[Process, None] = None

    def run_api(self) -> Process:
        api_prometheus_process: Process = Process(target=self._run_core, args=(self.__queue_data_bridge, self.__host, self.__port, self.__location, self.__buffer_cleaning_interval, ))
        api_prometheus_process.start()
        self.__logger.debug(f"Poppy prometheus API version: {self.__version} started")
        self.__logger.debug(f"Poppy prometheus API listening: http://{self.__host}:{self.__port}{self.__location}")
        self.__logger.debug(f"Poppy prometheus API buffer clearing period set to {self.__buffer_cleaning_interval}")
        self.__api_prometheus_process = api_prometheus_process
        return api_prometheus_process

    def _run_core(self, data_bridge_queue: Queue, host: str, port: str, location: str, buffer_cleaning_interval: int):
        self.__ApiCore: ApiCoreInterface = ApiCore(
            data_bridge_queue=data_bridge_queue,
            host=host,
            port=port,
            location=location,
            clearing_time=buffer_cleaning_interval
        )
        self.__ApiCore.run_core()

    def publish(self, api_prometheus_unit_list: list[ApiPrometheusUnitInterface]) -> None:
        self.__ApiPrometheusPublisher.publish(api_prometheus_unit_list)

    def revive(self) -> None:
        if not self.__api_prometheus_process.is_alive():
            is_alive_state = self.__api_prometheus_process.is_alive()
            self.__logger.warning(f"Try to revive API. Reason: API is alive -> {is_alive_state}")
            self.__api_prometheus_process.start()
            self.__logger.warning(f"API process revived successfully")

    def is_alive(self) -> bool:
        return self.__api_prometheus_process.is_alive()

    def is_alive_with_exception(self) -> None:
        if not self.__api_prometheus_process.is_alive():
            raise OperationIncompleteException(f"Poppy prometheus API terminated unexpectedly")

    def terminate(self):
        if self.__api_prometheus_process.is_alive():
            self.__api_prometheus_process.terminate()
            self.__api_prometheus_process.join()
            if not self.__api_prometheus_process.is_alive():
                self.__logger.debug(f"Poppy prometheus API terminated successfully")
            else:
                raise OperationIncompleteException(f"Poppy prometheus API terminated unsuccessfully")
        else:
            self.__logger.warning(f"Poppy prometheus API terminated before call")

    def get_version(self) -> str:
        return self.__version
