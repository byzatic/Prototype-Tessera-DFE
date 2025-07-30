#
#
#
from marshmallow import Schema, fields, post_load
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesConsistency


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesConsistency(Schema):
    position = fields.Integer(required=True)
    name = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesConsistency(**data)
