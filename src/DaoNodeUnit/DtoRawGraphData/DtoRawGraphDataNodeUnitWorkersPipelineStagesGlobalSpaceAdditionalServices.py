#
#
#
from .DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices:
    id_name: str
    description: str
    options: List[DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]
