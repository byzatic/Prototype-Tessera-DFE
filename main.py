#!/usr/bin/env python3.9
#
#
#
# logging
import logging

# DevelopToolBox
from src.DevelopToolBox.ApplicationStatic import ApplicationStatic

# LibByzaticCommon.Exceptions
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from src.LibByzaticCommon.Exceptions.ExitHandlerException import ExitHandlerException

# LibByzaticCommon.LoggingManager
from src.LibByzaticCommon.LoggingManager.LoggingManager import LoggingManager

from Global2p2.InterfaceApplicationContext import InterfaceApplicationContext
from ApplicationContext import ApplicationContext

from ServicePrometheus.impl_ServicePrometheus import impl_ServicePrometheus
from ServicePrometheus.i_ServicePrometheus import i_ServicePrometheus


def main():
    try:
        # [INITIALISATION] [app static]
        application_static = ApplicationStatic(__file__)

        # [INITIALISATION] [logger]
        logging_manager: LoggingManager = LoggingManager()
        logging_manager.init_logging(
            application_static.get("DEFINE_LOGGER_CONFIG_FILE_PATH_JSON"),
            "JSON"
        )
        applogger = logging.getLogger("Application-logger")
        init_info_logger = logging.getLogger("InitInfo-logger")

        # [INITIALISATION] [logging app info]
        app_version = application_static.get("APPLICATION_VERSION")
        init_info_logger.info(f"Starting service METRICS CORE GEN 2...")
        init_info_logger.info(f"app version: {app_version}")
        init_info_logger.info(f"app run 🚀...")

        applogger.debug(f"Creating context")
        app_context: InterfaceApplicationContext = ApplicationContext()
        applogger.debug(f"Creating service prometheus")
        service_prometheus: i_ServicePrometheus = impl_ServicePrometheus(app_context)
        applogger.debug(f"Start service prometheus")
        service_prometheus.run_service()

    except OperationIncompleteException as oie:
        raise ExitHandlerException(oie.args, errno=oie.errno, exception=oie)
    except Exception as e:
        raise ExitHandlerException(e.args, exception=e)
    except KeyboardInterrupt as ki:
        raise ExitHandlerException(ki.args, exception=ki)


if __name__ == '__main__':
    main()
