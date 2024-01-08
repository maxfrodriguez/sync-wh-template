# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(open_shipment_timmer) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import azure.functions as func
import logging

from orjson import loads

from src.sync_tmp_events.ETL.sync_events_chaged import SyncronizerChagesInFact
from src.sync_tmp_events.extract.ExampleExtractInformationImpl import ExampleExtractInformationImpl
from src.sync_tmp_events.load.load_facade import LoadInformationIntoFacade
from src.sync_tmp_events.transform.TransformInformationImpl import TransformInformationImpl

fucnt_timmer = func.Blueprint()

#sync from timer trigger
@fucnt_timmer.timer_trigger(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
async def timer_trigger_fact(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    syncronizer = SyncronizerChagesInFact(
        extract_service=ExampleExtractInformationImpl()
        , transform_service=TransformInformationImpl()
        , load_service=LoadInformationIntoFacade()
        )

    # Act
    await syncronizer.syncronize_fact()