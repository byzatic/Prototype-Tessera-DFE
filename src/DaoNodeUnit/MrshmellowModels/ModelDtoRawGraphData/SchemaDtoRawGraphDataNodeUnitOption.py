#
#
#
from marshmallow import Schema, fields, post_load
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitOption


class SchemaDtoRawGraphDataNodeUnitOption(Schema):
    option_name = fields.String(required=True)
    option_value = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitOption(**data)
