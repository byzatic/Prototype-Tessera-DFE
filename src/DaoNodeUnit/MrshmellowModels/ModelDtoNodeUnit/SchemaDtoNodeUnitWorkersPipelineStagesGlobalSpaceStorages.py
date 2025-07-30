#
#
#
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesGlobalSpaceStorages
from .SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions import SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions


class SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStorages(Schema):
    id_name = fields.String(required=True)
    description = fields.String(required=True)
    options = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesGlobalSpaceStorages(**data)
