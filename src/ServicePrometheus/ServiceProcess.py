#
#
#
import logging

from Global2p2.InterfaceApplicationContext import InterfaceApplicationContext
from typing import Union
from multiprocessing import Process, Queue
from AdditionalPackages.ApiPrometheus import ApiPrometheusInterface, ApiPrometheus
from time import sleep
from ApplicationContext import ApplicationContext

from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.InterfaceNodeUnitDescriptionRepository import InterfaceNodeUnitDescriptionRepository
from Global2p1.InterfaceNodeUnitDescriptionIdRepository import InterfaceNodeUnitDescriptionIdRepository
from Global2p2.i_Storage import i_Storage
from Global2p2.i_StorageItem import i_StorageItem

from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions
from AdditionalPackages.ApiPrometheus import ApiPrometheusUnitInterface

from DomainService.DomainService import DomainService

from LibByzaticCommon import Exceptions
from ServicePrometheus.SupportMethods import SupportMethods
from ServicePrometheus.i_WorkerContext import i_WorkerContext
from ServicePrometheus.impl_WorkerContext import impl_WorkerContext

from ServicePrometheus.SupportMakePrometheusUnitListFromPrometheusStorageItemList import SupportMakePrometheusUnitListFromPrometheusStorageItemList


class ServiceProcess(object):
    def __init__(self, context: InterfaceApplicationContext, sleep: int, api_prometheus: ApiPrometheusInterface):
        self.__logger: logging.Logger = logging.getLogger("ServicePrometheus-logger")
        self.__service_process: Union[None, Process] = None
        self.__ApplicationContext: InterfaceApplicationContext = context
        self.__WorkerContext: i_WorkerContext = impl_WorkerContext(self.__ApplicationContext)
        self.__ApiPrometheus: ApiPrometheusInterface = api_prometheus
        self.__SupportMakePrometheusUnitListFromPrometheusStorageItemList: SupportMakePrometheusUnitListFromPrometheusStorageItemList = SupportMakePrometheusUnitListFromPrometheusStorageItemList()

    def run_process(self):
        try:
            self.__logger.debug(f"ServicePrometheus -> ServiceProcess: iterate")

            self.__logger.debug(
                f"ServiceProcess: ApplicationContext >> getNodeUnitRepository (loading NodeUnitRepository)")
            root_node_unit_repository: InterfaceNodeUnitDescriptionRepository = self.__ApplicationContext.getNodeUnitRepository()
            self.__logger.debug(
                f"ServiceProcess: ApplicationContext >> getNodeUnitRepository (loaded NodeUnitRepository)")

            self.__logger.debug(f"ServiceProcess: NodeUnitDescription >> root description request processing")
            root_node_unit_description: NodeUnitDescription = root_node_unit_repository.get_root_node_unit_description()
            self.__logger.debug(
                f"ServiceProcess: NodeUnitDescription >> requests' result is root description wit id: {root_node_unit_description.get_node_id()}")

            self.__logger.debug(
                f"ServiceProcess: ApplicationContext << setRootNodeDescription (setting of root node description with id {root_node_unit_description.get_node_id()})")
            self.__ApplicationContext.setRootNodeDescription(root_node_unit_description)
            self.__logger.debug(
                f"ServiceProcess: ApplicationContext << setRootNodeDescription (setting of root node description with id {root_node_unit_description.get_node_id()} complete)")

            self.__logger.debug(f"ServiceProcess: ApplicationContext >> getDomainService (loading DomainService)")
            domain_service: DomainService = self.__ApplicationContext.getDomainService()
            self.__logger.debug(f"ServiceProcess: ApplicationContext >> getDomainService (loaded DomainService)")

            while True:
                self.__logger.debug(f"ServiceProcess: DomainService << process() (run calculation)")
                domain_service.process()
                self.__logger.debug(f"ServiceProcess: DomainService << process() (finished calculation)")

                self.__logger.debug(f"ServiceProcess: ApplicationContext >> getNodeUnitRepository")
                node_unit_repository: InterfaceNodeUnitRepository = self.__ApplicationContext.getNodeUnitRepository()
                self.__logger.debug(f"ServiceProcess: ApplicationContext >> getNodeUnitRepository")

                prometheus_storage: i_Storage = self.__get_prometheus_storage(node_unit_repository, root_node_unit_description)

                prometheus_unit_list: list[i_StorageItem] = self.__get_prometheus_storage_unit_list(prometheus_storage)

                self.__ApiPrometheus.is_alive_with_exception()
                self.__ApiPrometheus.publish(self.__SupportMakePrometheusUnitListFromPrometheusStorageItemList.convert(prometheus_unit_list, "status"))

                self.__ApplicationContext.getStorageManager().recreate_storages()
                self.__ApplicationContext.getNodeUnitIterator().reset()
                sleep(15)

        except Exceptions.OperationIncompleteException as oie:
            self.__ApiPrometheus.terminate()
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            self.__ApiPrometheus.terminate()
            raise Exceptions.OperationIncompleteException(e.args)

    def __get_prometheus_storage(self, node_unit_repository: InterfaceNodeUnitRepository, root_node_unit_description: NodeUnitDescription):
        node_additional_services: list[
            NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices] = node_unit_repository.get_node_unit(
            root_node_unit_description
        ).get_workers_pipeline().get_global_space().get_additional_services()
        prometheus_api_service: NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices = SupportMethods.filter_additional_services_by_id_name(
            "Prometheus_API", node_additional_services
        )

        prometheus_api_service_options: list[
            NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions] = prometheus_api_service.get_options()
        prometheus_api_service_storage_name: str = SupportMethods.filter_additional_services_options_by_name(
            "storage", prometheus_api_service_options
        ).get_data()

        prometheus_storage: i_Storage = self.__ApplicationContext.getStorageManager().get_storage(prometheus_api_service_storage_name)
        return prometheus_storage

    def __get_prometheus_storage_unit_list(self, prometheus_storage: i_Storage) -> list[i_StorageItem]:
        prometheus_storage_list_keys = prometheus_storage.read_list_keys()
        prometheus_unit_list: list[i_StorageItem] = []
        for prometheus_storage_key in prometheus_storage_list_keys:
            prometheus_unit: i_StorageItem = prometheus_storage.read(prometheus_storage_key)
            prometheus_unit_list.append(prometheus_unit)
        self.__logger.debug(f"Generated {len(prometheus_unit_list)} items for prometheus")
        return prometheus_unit_list