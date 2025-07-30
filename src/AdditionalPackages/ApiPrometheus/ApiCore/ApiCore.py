#
#
#
import logging
from .ABCAbstractCollection import ApiCoreInterface
from flask import Flask, make_response, request, jsonify
from waitress import serve
from typing import Union
from multiprocessing import Queue
from copy import deepcopy
import _thread as low_level_threading
from datetime import datetime as dt
from time import sleep
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException


class ApiCore(ApiCoreInterface):
    def __init__(self, data_bridge_queue: Queue, host: str = "0.0.0.0", port: str = "8080", location: str = "/metrics", clearing_time: int = 30):
        self.__logger: logging.Logger = logging.getLogger("WSGI-logger")
        self.__app: Flask = Flask(__name__)
        self.__flask_log = logging.getLogger('werkzeug')
        self.__logger: logging.Logger = self.__flask_log
        self.__data_bridge_queue = data_bridge_queue
        self.default_there_is_no_data_msg: str = f"Sorry, there is no data yet ;)"
        self.__bridged_data = self.default_there_is_no_data_msg
        self.__server_host: str = host
        self.__server_port: str = port
        self.__location: str = location
        self.__clearing_time: int = clearing_time

    def run_core(self) -> None:
        self.__configure_logging()
        self.__core(self.__data_bridge_queue)
        self.__serve_app()

    def __configure_logging(self) -> None:
        self.__flask_log.disabled = True
        self.__app.logger.disabled = True

    def __core(self, data_bridge_queue: Queue, buffer_location: Union[str, None] = None):

        # maybe I need it
        buffer_location: Union[str, None] = buffer_location

        @self.__app.route(self.__location)
        def metrics():
            if (request.method == 'GET'):
                response_data = str(self.__bridged_data)
                response = make_response(response_data, 200)
                response.mimetype = "text/plain"
                self.__logger.debug(f"request method {request.method}")
                return response

        @self.__app.errorhandler(404)
        def not_found():
            return make_response(jsonify({'error': 'Not found'}), 404)

        self.__run_metrics_update(data_bridge_queue)

    def __run_metrics_update(self, data_bridge_queue: Queue):
        try:
            t_process = low_level_threading.start_new_thread(self.__metrics_update, (data_bridge_queue, self.__clearing_time,))
            self.__logger.debug(f"Started a new instance of metrics update function -> {t_process}")
        except low_level_threading.error as llte:
            raise OperationIncompleteException(llte)

    # TODO: May be there is high load bug! (look at sleep(0.01))
    def __metrics_update(self, data_bridge_queue: Queue, clearing_time: int = 30):
        s_ts = int(dt.utcnow().strftime("%s"))
        while True:
            sleep(0.01)
            if not data_bridge_queue.empty():
                bridged_data = data_bridge_queue.get()
                self.__bridged_data = deepcopy(bridged_data)
                s_ts = int(dt.utcnow().strftime("%s"))
            else:
                n_ts = int(dt.utcnow().strftime("%s"))
                r_ts: int = n_ts - s_ts
                if r_ts >= 0:
                    if r_ts > clearing_time:
                        self.__bridged_data = self.default_there_is_no_data_msg
                    else:
                        pass
                else:
                    raise OperationIncompleteException(f"Undefined error "
                                                       f"while calculate time of "
                                                       f"clearing data in buffer -> {n_ts} {s_ts}")

    def __serve_app(self, host: str = "0.0.0.0", port: str = "8080"):
        # production WSGI server
        self.__logger.debug(f"Starting API WSGI server on http://{host}:{port}{self.__location}")
        serve(self.__app, host=host, port=port)

    def __serve_app_development(self, host: str = "0.0.0.0", port: int = 8080, debug: bool = True):
        # development default flask web server
        self.__logger.debug(f"Starting API default flask web server server on http://{host}:{port}{self.__location}")
        self.__app.run(debug=debug, host=host, port=port)
