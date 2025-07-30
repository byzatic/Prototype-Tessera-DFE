#
#
#
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union
from typing import Optional


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit:
    abstract_data_type: Optional[str] = None
    abstract_data_specialty: Optional[str] = None
    abstract_data_path: Optional[str] = None
    abstract_data_key: Optional[str] = None
    abstract_data_value: Optional[str] = None
