#
#
#
from .SchemaDtoNodeUnitWorkersPipelineStagesDescription import SchemaDtoNodeUnitWorkersPipelineStagesDescription
from .SchemaDtoNodeUnitWorkersPipelineStagesConsistency import SchemaDtoNodeUnitWorkersPipelineStagesConsistency
from .SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpace import SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpace
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipeline


class SchemaDtoNodeUnitWorkersPipeline(Schema):
    stages_consistency = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesConsistency, required=True))
    stages_description = fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesDescription, required=True)
    global_space = fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpace, required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipeline(**data)
