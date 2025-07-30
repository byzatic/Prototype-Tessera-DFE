#
#
#
import logging

from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions


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
