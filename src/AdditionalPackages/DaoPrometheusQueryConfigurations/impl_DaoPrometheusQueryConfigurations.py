#
#
#
import logging
from copy import deepcopy
from .i_DaoPrometheusQueryConfigurations import i_DaoPrometheusQueryConfigurations
from LibByzaticCommon.FileReaders.ABCAbstractCollection import BaseReaderInterface
from LibByzaticCommon.FileReaders import JsonFileReader
from .MrshmellowModels.ModelPrometheusQueryConfiguration.SchemaPrometheusQueryConfiguration import SchemaPrometheusQueryConfiguration
from AdditionalPackages.DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration.PrometheusQueryConfiguration import PrometheusQueryConfiguration
from LibByzaticCommon import Exceptions

class impl_DaoPrometheusQueryConfigurations(i_DaoPrometheusQueryConfigurations):
    def __init__(self, prometheus_query_configuration_file_path: str):
        self.__logger: logging.Logger = logging.getLogger("DaoNodeDataRaw-logger")
        self.__prometheus_query_configuration_file_path: str = prometheus_query_configuration_file_path
        self.__JsonFileReader: BaseReaderInterface = JsonFileReader()
        self.__prometheus_query_unit_list: list[PrometheusQueryConfiguration] = []
        self.__PrometheusQueryConfigurationMrshmellowModel: SchemaPrometheusQueryConfiguration = SchemaPrometheusQueryConfiguration()
        self.__create_query_unit_list()

    def __create_query_unit_list(self):
        try:
            raw_data: list = self.__JsonFileReader.read(self.__prometheus_query_configuration_file_path)
            for raw_data_unit in raw_data:
                unmarshalled_unit: PrometheusQueryConfiguration = self.__PrometheusQueryConfigurationMrshmellowModel.load(raw_data_unit)
                if unmarshalled_unit is not None:
                    self.__prometheus_query_unit_list.append(unmarshalled_unit)
                else:
                    Exceptions.OperationIncompleteException(f"unmarshalled query unit is none")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)

    def getPrometheusQueryConfigurationUnit(self, query_id: str) -> PrometheusQueryConfiguration:
        try:
            for query_unit_description in self.__prometheus_query_unit_list:
                for query_unit in query_unit_description.getQueryDescription():
                    if str(query_unit.getQueryId()) == query_id:
                        return query_unit_description
            raise Exceptions.OperationIncompleteException(f"PrometheusQueryConfigurationUnit with Query with id {query_id} not found")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)

    def getAllPrometheusQueryConfigurationUnits(self) -> list[PrometheusQueryConfiguration]:
        try:
            return self.__prometheus_query_unit_list
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)
