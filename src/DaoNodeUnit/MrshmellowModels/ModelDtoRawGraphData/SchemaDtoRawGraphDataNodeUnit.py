#
#
from .SchemaDtoRawGraphDataNodeUnitOption import SchemaDtoRawGraphDataNodeUnitOption
from .SchemaDtoRawGraphDataNodeUnitWorkersPipeline import SchemaDtoRawGraphDataNodeUnitWorkersPipeline
from marshmallow import Schema, fields, post_load
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnit


class SchemaDtoRawGraphDataNodeUnit(Schema):
    options = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitOption, many=False, required=True))
    workers_pipeline = fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipeline, many=False, required=True)
    downstream = fields.List(fields.Nested("SchemaDtoRawGraphDataNodeUnit", required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnit(**data)
