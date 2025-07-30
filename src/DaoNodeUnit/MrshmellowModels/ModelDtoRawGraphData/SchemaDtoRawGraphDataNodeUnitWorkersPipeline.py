#
#
#
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescription import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescription
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesConsistency import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesConsistency
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpace import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpace
from marshmallow import Schema, fields, post_load
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipeline


class SchemaDtoRawGraphDataNodeUnitWorkersPipeline(Schema):
    global_space = fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpace, required=True)
    stages_consistency = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesConsistency, required=True))
    stages_description = fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescription, required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipeline(**data)
