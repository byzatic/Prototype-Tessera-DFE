#
#
#
from .DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData import DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo:
    stage_id: str
    stage_data: List[DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData]
