from datetime import datetime
from typing import Generator, List


from common.common_infrastructure.dataaccess.db_profit_tools_access.pt_anywhere_client import PTSQLAnywhere
from common.common_infrastructure.dataaccess.db_ware_house_access.whdb_anywhere_client import WareHouseDbConnector

from src.sync_tmp_events.extract.data.ExampleDTO import ExampleDTO

from src.sync_tmp_events.extract.queries.query_event_pt import EXAMPLE_UPDATE_QUERY
from src.sync_tmp_events.extract.contracts.facade_extract_abc import ExtractFacadeABC



class ExampleExtractInformationUpdateImpl(ExtractFacadeABC):

    def __init__(self) -> None:
        self.wh_repository = WareHouseDbConnector()
        #self.pt_repository = PTSQLAnywhere()


    async def get_fact_information(self, reference_data : list[dict] = None) -> None:

        de_ids = set(events_changed["de_id"] for events_changed in reference_data)
        ids = ", ".join(f"{de_id}" for de_id in de_ids)

        async with self.wh_repository:
            raw_data = self.wh_repository.execute_select(
                EXAMPLE_UPDATE_QUERY.format(
                    de_ids = ids
                )
            )

        self.data_to_sync = [ExampleDTO(**rawExampleDTO) for rawExampleDTO in raw_data]
        self.data_to_sync.sort(key=lambda x: x.ds_id)