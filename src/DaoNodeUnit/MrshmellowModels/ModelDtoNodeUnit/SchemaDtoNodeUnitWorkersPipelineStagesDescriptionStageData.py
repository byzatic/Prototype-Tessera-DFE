#
#
#
from .SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from .SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesDescriptionStageData


class SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageData(Schema):
    name = fields.String(required=True)
    configuration = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit, required=True))
    abstract_data_list = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesDescriptionStageData(**data)
