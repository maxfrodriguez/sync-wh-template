from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from common.common_infrastructure.cross_cutting.dt_converter import DTConverter

@dataclass
class IAbstractDTO:
    id: int = -1
    created_at_str: str = None
    updated_at_str: str = None
    created_at: datetime = datetime.utcnow().replace(second=0, microsecond=0)
    updated_at: datetime = datetime.utcnow().replace(second=0, microsecond=0)
    hash: str = None

    def __post_init__(self):
        if self.created_at_str:
            self.created_at = DTConverter.str_to_utc_dt(self.created_at_str)
        if self.updated_at_str:
            self.updated_at = DTConverter.str_to_utc_dt(self.updated_at_str)
    
