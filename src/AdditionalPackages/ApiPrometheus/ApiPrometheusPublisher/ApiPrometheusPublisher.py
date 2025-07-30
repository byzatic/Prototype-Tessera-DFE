#
#
#
import logging
from time import sleep
from .ABCAbstractCollection import ApiPrometheusPublisherInterface
from multiprocessing import Queue
from ..ApiPrometheusUnit import ApiPrometheusUnitInterface
from ..ApiPrometheusUnitTransform import ApiPrometheusUnitTransform, ApiPrometheusUnitTransformInterface
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ApiPrometheusPublisher(ApiPrometheusPublisherInterface):
    def __init__(self, data_bridge_queue: Queue):
        self.__logger: logging.Logger = logging.getLogger("ApiPrometheus-logger")
        self.__data_bridge_queue: Queue = data_bridge_queue
        self.__ApiPrometheusUnitTransform: ApiPrometheusUnitTransformInterface = ApiPrometheusUnitTransform()
        self.__queue_put_limit: int = 100
        self.__queue_put_counter: int = 0

    def publish(self, api_prometheus_unit_list: list[ApiPrometheusUnitInterface]) -> None:
        try:
            unit_string_list: list = []
            for api_prometheus_unit in api_prometheus_unit_list:
                unit_string = self.__ApiPrometheusUnitTransform.transform(api_prometheus_unit)
                unit_string_list.append(unit_string)
            pt_unit_string = '\n'.join(map(str, unit_string_list))
            self.__queue_put(pt_unit_string)
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise OperationIncompleteException(e.args)

    def __queue_put(self, data, put_time_wait: float = 0.33):
        if self.__queue_put_counter > self.__queue_put_limit:
            self.__logger.error((f"Internal API error: queue not empty "
                                 f"before {self.__queue_put_limit} attempts, "
                                 f"with put_time_wait {put_time_wait}"))
            raise OperationIncompleteException(f"Internal API error: queue not empty "
                                               f"before {self.__queue_put_limit} attempts, "
                                               f"with put_time_wait {put_time_wait}")
        else:
            if self.__data_bridge_queue.empty():
                self.__data_bridge_queue.put(data)
                self.__queue_put_counter = 0
            else:
                sleep(put_time_wait)
                self.__queue_put(data, put_time_wait)
