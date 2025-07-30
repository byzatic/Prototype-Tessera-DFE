#
#
#
from .DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo import DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesDescription:
    stages_info: List[DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo]
