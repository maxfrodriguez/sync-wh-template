from datetime import datetime, timedelta
import pytest

from src.sync_tmp_events.ETL.sync_events_chaged import SyncronizerChagesInFact
from src.sync_tmp_events.ETL.sync_events_updated import SyncronizerUpdatesInFact
from src.sync_tmp_events.extract.ExampleExtractInformationImpl import ExampleExtractInformationImpl
from src.sync_tmp_events.extract.ExampleExtractInformationUpdateImpl import ExampleExtractInformationUpdateImpl
from src.sync_tmp_events.load.load_facade import LoadInformationIntoFacade
from src.sync_tmp_events.transform.TransformInformationImpl import TransformInformationImpl
from src.sync_tmp_events.transform.TransformInformationUpdateImpl import TransformInformationUpdateImpl


@pytest.mark.asyncio
class TestSyncronizerEvents:

    async def test_syncronizer_no_data_trigger(self): 
        # Arrange
        start_dt = "2024-01-03"
        end_dt = "2024-01-03"
        
        start_dt = datetime.strptime(start_dt, '%Y-%m-%d').replace(hour=2, minute=59, second=59, microsecond=0)
        end_dt = datetime.strptime(end_dt, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=0) + timedelta(hours=3)

        syncronizer = SyncronizerChagesInFact(
            extract_service=ExampleExtractInformationImpl(
                p_start_dt=start_dt
                , p_end_dt=end_dt
            )
            , transform_service=TransformInformationImpl()
            , load_service=LoadInformationIntoFacade()
            )

        # Act
        await syncronizer.syncronize_fact()

        # Assert
        assert syncronizer != None

    async def test_load_events_open(self):
        # Arrange
        #Sync from timer trigger without data
        tmps = [
            {"de_id":830498, "ds_id": 152983},
        ]

        # Act
        syncronizer = SyncronizerUpdatesInFact(
            extract_service=ExampleExtractInformationUpdateImpl()
            , transform_service=TransformInformationUpdateImpl()
            , load_service=LoadInformationIntoFacade()
            )

        # Act
        await syncronizer.syncronize_fact(reference_data = tmps)

        # Assert
        assert syncronizer != None
