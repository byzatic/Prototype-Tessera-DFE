#
#
#
import logging
from typing import Optional

from .ABCAbstractCollection import PrometheusQueryTemplateUnitRepositoryInterface
from src.LibByzaticCommon.Exceptions.OperationIncompleteException import OperationIncompleteException
from .PrometheusQueryTemplateUnit import PrometheusQueryTemplateUnitInterface, PrometheusQueryTemplateUnit
from .QueryTemplates.QueryTemplates import PROMETHEUS_QUERIES


class PrometheusQueryTemplateUnitRepository(PrometheusQueryTemplateUnitRepositoryInterface):
    def __init__(self) -> None:
        self.__logger: logging.Logger = logging.getLogger("PrometheusQueryTemplateUnitRepository-logger")
        self.__prometheus_queries: dict = PROMETHEUS_QUERIES

    def get(self, query_name: Optional[str] = None) -> PrometheusQueryTemplateUnitInterface:
        try:
            query_template_unit: PrometheusQueryTemplateUnitInterface
            if query_name is None or query_name == "":
                raise OperationIncompleteException(f"Query name is not defined")
            else:
                if query_name in self.__prometheus_queries:
                    query_template_unit = self.__create_query_template_unit(query_name)
                else:
                    raise OperationIncompleteException(f"No such query {query_name}")
            return query_template_unit
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def get_list_all_available_query_template_unit(self) -> list[PrometheusQueryTemplateUnitInterface]:
        try:
            query_template_unit_list: list[PrometheusQueryTemplateUnitInterface] = (
                self.__create_list_all_available_query_template_unit())
            return query_template_unit_list
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)


    def __create_query_template_unit(self, query_name: str) -> PrometheusQueryTemplateUnitInterface:
        try:
            query_template_unit: PrometheusQueryTemplateUnitInterface = PrometheusQueryTemplateUnit(
                query_name=query_name,
                query_template=self.__prometheus_queries[query_name]
            )
            return query_template_unit
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

    def __create_list_all_available_query_template_unit(self) -> list[PrometheusQueryTemplateUnitInterface]:
        try:
            query_template_unit_list: list[PrometheusQueryTemplateUnitInterface] =[]
            for query_name, query_body in self.__prometheus_queries.items():
                query_template_unit: PrometheusQueryTemplateUnitInterface = PrometheusQueryTemplateUnit(
                    query_name=query_name,
                    query_template=query_body
                )
                query_template_unit_list.append(query_template_unit)
            return query_template_unit_list
        except OperationIncompleteException as oie:
            raise OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise OperationIncompleteException(err.args)

