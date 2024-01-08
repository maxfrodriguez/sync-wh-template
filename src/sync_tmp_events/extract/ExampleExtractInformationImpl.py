from datetime import datetime
from typing import Generator, List


from common.common_infrastructure.dataaccess.db_profit_tools_access.pt_anywhere_client import PTSQLAnywhere
from common.common_infrastructure.dataaccess.db_ware_house_access.whdb_anywhere_client import WareHouseDbConnector

from src.sync_tmp_events.extract.data.ExampleDTO import ExampleDTO

from src.sync_tmp_events.extract.queries.query_event_pt import EXAMPLE_EXTRACT_QUERY
from src.sync_tmp_events.extract.contracts.facade_extract_abc import ExtractFacadeABC



class ExampleExtractInformationImpl(ExtractFacadeABC):

    def __init__(self, p_start_dt: datetime, p_end_dt: datetime) -> None:
        self.wh_repository = WareHouseDbConnector()
        #self.pt_repository = PTSQLAnywhere()

        self.start_dt = p_start_dt
        self.end_dt = p_end_dt


    async def get_fact_information(self, reference_data : list[dict] = None) -> None:

        async with self.wh_repository:
            raw_data = self.wh_repository.execute_select(
                EXAMPLE_EXTRACT_QUERY.format(
                    start_dt = self.start_dt.strftime("%Y-%m-%d %H:%M:%S")
                    , end_dt = self.end_dt.strftime("%Y-%m-%d %H:%M:%S")
                )
            )

        self.data_to_sync = [ExampleDTO(**rawExampleDTO) for rawExampleDTO in raw_data]
        self.data_to_sync.sort(key=lambda x: x.ds_id)