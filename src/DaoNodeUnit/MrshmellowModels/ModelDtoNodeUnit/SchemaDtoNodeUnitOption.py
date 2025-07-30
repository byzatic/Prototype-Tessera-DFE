#
#
#
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitOption


class SchemaDtoNodeUnitOption(Schema):
    option_name = fields.String(required=True)
    option_value = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitOption(**data)
