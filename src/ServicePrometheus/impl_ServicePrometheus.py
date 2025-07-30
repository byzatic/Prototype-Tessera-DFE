#
#
#
from .i_ServicePrometheus import i_ServicePrometheus
from Global2p2.InterfaceApplicationContext import InterfaceApplicationContext
from typing import Optional
from multiprocessing import Process, Queue
from AdditionalPackages.ApiPrometheus import ApiPrometheusInterface, ApiPrometheus
from ServiceProcess import ServiceProcess
from LibByzaticCommon import Exceptions
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions
from Global2p1.NodeUnit.NodeUnit import NodeUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices


class impl_ServicePrometheus(i_ServicePrometheus):
    def __init__(self, context: InterfaceApplicationContext):
        self.__service_id_name: str = "Prometheus_API"
        self.__context: InterfaceApplicationContext = context
        self.__ApiPrometheus: ApiPrometheusInterface = self.__init_api_prometheus()
        self.__ServiceProcess = ServiceProcess(self.__context, 5, self.__ApiPrometheus)

    def run_service(self) -> None:
        self.__ApiPrometheus.run_api()
        self.__ServiceProcess.run_process()

    def __init_api_prometheus(self) -> ApiPrometheusInterface:
        try:
            api_prometheus_parameters_list: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions] = self.__get_api_prometheus_parameters_list(self.__context)
            api_prometheus: ApiPrometheusInterface = ApiPrometheus(
                host=self.__get_api_prometheus_host(api_prometheus_parameters_list),
                port=self.__get_api_prometheus_port(api_prometheus_parameters_list),
                location=self.__get_api_prometheus_location(api_prometheus_parameters_list),
                buffer_cleaning_interval=self.__get_api_prometheus_buffer_cleaning_interval(api_prometheus_parameters_list)
            )
            return api_prometheus
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)

    def __get_api_prometheus_parameters_list(self, context: InterfaceApplicationContext) -> list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]:
        api_prometheus_parameters_list: Optional[list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]] = None
        root_node_unit: NodeUnit = context.getNodeUnitRepository().get_root_node_unit()
        found_additional_service: Optional[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices] = None
        for additional_service in root_node_unit.get_workers_pipeline().get_global_space().get_additional_services():
            if additional_service.get_id_name() == self.__service_id_name:
                found_additional_service = additional_service
        if found_additional_service is not None:
            api_prometheus_parameters_list = found_additional_service.get_options()
            return found_additional_service.get_options()
        else:
            raise Exceptions.OperationIncompleteException(f"Service with id_name {self.__service_id_name} not found")

    def __get_api_prometheus_host(self, api_prometheus_parameters_list: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]) -> str:
        parameter: Optional[str] = None
        for api_prometheus_parameter in api_prometheus_parameters_list:
            if api_prometheus_parameter.get_name() == "API_LISTENING_ADDRESS":
                parameter = api_prometheus_parameter.get_data()
        if parameter is not None:
            return parameter
        else:
            raise Exceptions.OperationIncompleteException(f"Service's parameter API_LISTENING_ADDRESS not found")

    def __get_api_prometheus_port(self, api_prometheus_parameters_list: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]) -> str:
        parameter: Optional[str] = None
        for api_prometheus_parameter in api_prometheus_parameters_list:
            if api_prometheus_parameter.get_name() == "API_PORT":
                parameter = api_prometheus_parameter.get_data()
        if parameter is not None:
            return parameter
        else:
            raise Exceptions.OperationIncompleteException(f"Service's parameter API_PORT not found")

    def __get_api_prometheus_location(self, api_prometheus_parameters_list: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]) -> str:
        parameter: Optional[str] = None
        for api_prometheus_parameter in api_prometheus_parameters_list:
            if api_prometheus_parameter.get_name() == "API_LOCATION":
                parameter = api_prometheus_parameter.get_data()
        if parameter is not None:
            return parameter
        else:
            raise Exceptions.OperationIncompleteException(f"Service's parameter API_LOCATION not found")

    def __get_api_prometheus_buffer_cleaning_interval(self, api_prometheus_parameters_list: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]) -> int:
        parameter: Optional[int] = None
        for api_prometheus_parameter in api_prometheus_parameters_list:
            if api_prometheus_parameter.get_name() == "API_BUFFER_CLEAN_INTERVAL_SECONDS":
                str_parameter: str = api_prometheus_parameter.get_data()
                if str_parameter.isdigit():
                    parameter = int(str_parameter)
                else:
                    raise Exceptions.OperationIncompleteException(f"Service's parameter API_BUFFER_CLEAN_INTERVAL_SECONDS is wrong type (not digit)")
        if parameter is not None:
            return parameter
        else:
            raise Exceptions.OperationIncompleteException(f"Service's parameter API_BUFFER_CLEAN_INTERVAL_SECONDS not found")
