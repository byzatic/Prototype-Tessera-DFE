from unittest import TestCase

from Global2p2.InterfaceApplicationContext import InterfaceApplicationContext
from ApplicationContext import ApplicationContext

from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.InterfaceNodeUnitDescriptionRepository import InterfaceNodeUnitDescriptionRepository
from Global2p1.InterfaceNodeUnitDescriptionIdRepository import InterfaceNodeUnitDescriptionIdRepository

from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions

class TestApplicationContext(TestCase):
    def test_get_dao_node_unit_from_rest(self):

        # Prometheus node request
        prom_node_request = "x"

        # Worker Context initialisation
        ctx: InterfaceApplicationContext
        ctx = ApplicationContext()
        # ctx.__RootNodeUnitDescription -> 1 (predefined root node description)

        # get new root node by prometheus node request
        root_node_unit_repository: InterfaceNodeUnitDescriptionIdRepository = ctx.getNodeUnitRepository()
        root_node_unit_description: NodeUnitDescription = root_node_unit_repository.get_node_unit_description_by_id(prom_node_request)
        ctx.setRootNodeDescription(root_node_unit_description)
        # ctx.__RootNodeUnitDescription -> 2 (use cases' root node description)

        # DomainService process graph
        ctx.getDomainService().process()

        # get data
        node_unit_repository: InterfaceNodeUnitRepository = ctx.getNodeUnitRepository()

        node_additional_services: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices] = node_unit_repository.get_node_unit(
            root_node_unit_description
        ).get_workers_pipeline().get_global_space().get_additional_services()
        prometheus_api_service: NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices = SupportMethods.filter_additional_services_by_id_name("prometheus_api", node_additional_services)

        prometheus_api_service_options: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions] = prometheus_api_service.get_options()
        prometheus_api_service_storage_name: str = SupportMethods.filter_additional_services_options_by_name("storage", prometheus_api_service_options).get_data()

        expected_data = ctx.get_storage_manager().get_storage_by_name("output_storage_descr").get_data()


        def __filter_additional_services_by_id_name(id_name: str, node_additional_services: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices]) -> NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices:
            for node_additional_service in node_additional_services:
                if node_additional_service.get_id_name() == id_name:
                    return node_additional_service


        self.fail()


    def test_get_dao_node_unit_from_prometheus(self):

        # smth prepare for root
        ctx: InterfaceApplicationContext.ApplicationContext # root = 1
        ctx = InterfaceApplicationContext()

        # process
        ctx.getDomainService().process()

        # get data
        output_storage_descr = ctx.getInterfaceNodeUnitRepository().get_node_unit(
            ctx.getInterfaceNodeUnitRepository().get_top_level_root_node() # -> description
        ).get_workers_pipeline().get_global_space().get_additional_services().filter_by_id_name("prometheus_api").get_options().filter_by_name("storage").get_data()


        expected_data = ctx.get_storage_manager().get_storage_by_name("output_storage_descr").get_data()


        self.fail()


        # TODO: filter in node_unit

class SupportMethods(object):
    def __init__(self):
        pass

    @staticmethod
    def filter_additional_services_by_id_name(id_name: str, node_additional_services: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices]) -> NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices:
        for node_additional_service in node_additional_services:
            if node_additional_service.get_id_name() == id_name:
                return node_additional_service

    @staticmethod
    def filter_additional_services_options_by_name(name: str, prometheus_api_service_options: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]) -> NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions:
        for prometheus_api_service_option_item in prometheus_api_service_options:
            if prometheus_api_service_option_item.get_name() == name:
                return prometheus_api_service_option_item
