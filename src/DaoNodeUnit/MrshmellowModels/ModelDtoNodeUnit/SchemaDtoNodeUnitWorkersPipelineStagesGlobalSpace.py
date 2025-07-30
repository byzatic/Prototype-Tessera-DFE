#
#
#
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesGlobalSpace
from .SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStorages import SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStorages
from .SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices import SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices


class SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpace(Schema):
    storages = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStorages, required=True))
    additional_services = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesGlobalSpace(**data)
