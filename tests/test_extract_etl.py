import pytest
from datetime import datetime

from src.sync_tmp_events.extract.ExampleExtractInformationImpl import ExampleExtractInformationImpl

@pytest.mark.asyncio
class TestExtractInformation:
    
    async def test_extract_data(self): 

        start_dt = "2024-01-03"
        end_dt = "2024-01-03"
        
        start_dt = datetime.strptime(start_dt, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = datetime.strptime(end_dt, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=0)

        #Arrange
        extract_service = ExampleExtractInformationImpl(start_dt, end_dt)

        #act
        await extract_service.get_fact_information()
        #get the results from next_fact_to_sync from generator

        await extract_service.set_pack_size()
        for results in extract_service.next_fact_to_sync():
            pass

        #assert
        assert extract_service.data_to_sync != None
        assert len(extract_service.data_to_sync) > 0
