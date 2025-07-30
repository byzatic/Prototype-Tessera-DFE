#
#
#
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions:
    name: str
    data: str
