#
#
#
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices
from .SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions


class SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices(Schema):
    id_name = fields.String(required=True)
    description = fields.String(required=True)
    options = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices(**data)
