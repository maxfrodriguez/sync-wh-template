import logging
from typing import List

from orjson import dumps, loads

from common.common_infrastructure.dataaccess.db_ware_house_access.whdb_anywhere_client import WareHouseDbConnector

from src.sync_tmp_events.load.contracts.facade_load_abc import LoadFacadeABC
from src.sync_tmp_events.load.data.SAFactExample import SAFactExample
from src.sync_tmp_events.load.data.ExampleAdapter import ExampleAdapter

from src.sync_tmp_events.extract.contracts.IAbstractDTO import IAbstractDTO


class LoadInformationIntoFacade(LoadFacadeABC):
    def __init__(self) -> None:
        super().__init__()
        self.wh_repository = WareHouseDbConnector()
        self.sa_to_Load: List[SAFactExample] = []

    async def load_fact(self, data_to_load: List[IAbstractDTO]):
        
        async with self.wh_repository:
            for exampleData in data_to_load:
                try:
                    self.sa_to_Load.append(ExampleAdapter(
                        **loads(dumps(exampleData))
                    ))

                    self.data_to_notify.append(exampleData)
                except Exception as e:
                    logging.error(f"Error sincronizing events {exampleData.de_id}: {e}")

            try:
                async with self.wh_repository:
                    self.wh_repository.upsert_data(model_instances=self.sa_to_Load)
                #self.wh_repository.bulk_copy(self.bulk_events)
            except Exception as e:
                ids = ", ".join(f"'{shipment.ds_id}'" for shipment in data_to_load)
                raise Exception(f"Error in bulk_copy and sync to warehouse the shipments: {ids}, with error: {e}")

    
    async def delete_events(self, data_to_delete: List[IAbstractDTO]) -> None:
        raise NotImplementedError
    
    async def notify_changes(self) -> None:
        raise NotImplementedError