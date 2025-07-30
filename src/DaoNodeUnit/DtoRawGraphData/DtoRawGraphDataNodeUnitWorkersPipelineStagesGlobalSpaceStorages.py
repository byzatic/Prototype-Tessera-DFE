#
#
#
from .DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions import DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStorages:
    id_name: str
    description: str
    options: List[DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions]
