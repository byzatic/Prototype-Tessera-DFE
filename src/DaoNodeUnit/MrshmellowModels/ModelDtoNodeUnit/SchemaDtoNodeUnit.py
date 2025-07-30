#
#
from .SchemaDtoNodeUnitOption import SchemaDtoNodeUnitOption
from .SchemaDtoNodeUnitWorkersPipeline import SchemaDtoNodeUnitWorkersPipeline
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnit


class SchemaDtoNodeUnit(Schema):
    options = fields.List(fields.Nested(SchemaDtoNodeUnitOption, many=False, required=True))
    workers_pipeline = fields.Nested(SchemaDtoNodeUnitWorkersPipeline, many=False, required=True)
    downstream = fields.List(fields.Nested("SchemaDtoNodeUnit", required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnit(**data)
