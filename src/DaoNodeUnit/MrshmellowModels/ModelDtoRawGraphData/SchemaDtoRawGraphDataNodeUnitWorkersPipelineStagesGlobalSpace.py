#
#
#
from marshmallow import Schema, fields, post_load
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpace
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStorages import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStorages
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpace(Schema):
    storages = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStorages, required=True))
    additional_services = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpace(**data)
