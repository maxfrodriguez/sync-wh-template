from typing import Any, Dict, List

from src.sync_tmp_events.extract.contracts.IAbstractDTO import IAbstractDTO
from src.sync_tmp_events.extract.data.ExampleDTO import ExampleDTO
from src.sync_tmp_events.transform.contracts.facade_transform_abc import TransformFacadeABC

#from common.common_infrastructure.dataaccess.db_ware_house_access.whdb_anywhere_client import WareHouseDbConnector

class TransformInformationUpdateImpl(TransformFacadeABC):
    def __init__(self) -> None:
        super().__init__()
        #self.wh_repository = WareHouseDbConnector()


    async def transform_fact_to_sync(self, data_to_transform: List[ExampleDTO]) -> None:
        for data in data_to_transform:
            if not data.arrival_date:
                data.status = "Cancelled"
            elif data.schedule_date <= data.arrival_date:
                data.status = "Delivered"
            elif data.schedule_date >= data.arrival_date:
                data.status = "Missed"
            
            self.data_to_transform.append(data)