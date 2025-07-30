#
#
#
from marshmallow import Schema, fields, post_load
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStorages
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStorages(Schema):
    id_name = fields.String(required=True)
    description = fields.String(required=True)
    options = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStorages(**data)
