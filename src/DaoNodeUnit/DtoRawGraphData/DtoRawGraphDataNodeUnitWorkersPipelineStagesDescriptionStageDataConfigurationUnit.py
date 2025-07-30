#
#
#
from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit:
    abstract_data_type: str
    abstract_data_specialty: str
    abstract_data_path: str
    abstract_data_key: str
    abstract_data_value: str
