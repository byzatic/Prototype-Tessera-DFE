#
#
#
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions:
    name: str
    data: str
