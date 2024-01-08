from dataclasses import dataclass
from datetime import datetime
from common.common_infrastructure.cross_cutting.dt_converter import DTConverter

from src.sync_tmp_events.extract.contracts.IAbstractDTO import IAbstractDTO


@dataclass
class ExampleDTO(IAbstractDTO):
    ds_id: int = None
    de_id: int = None
    de_ship_seq: int = None
    ev_de_appointment : datetime = None
    schedule_date_str : str = None
    schedule_date : datetime = None
    arrival_date : datetime = None
    driver_id : int = None
    ds_id_snapshot: int = None
    de_id_snapshot : int = None
    status: str = None

    def __post_init__(self):
        super().__post_init__()

        if self.schedule_date_str:
            self.schedule_date = DTConverter.str_to_pst_dt(self.schedule_date_str)
        else:
            self.schedule_date = DTConverter.dt_to_pst_dt(self.schedule_date)

    def calculate_fields(self):
        #this method is to Generate 
        raise NotImplementedError

        
