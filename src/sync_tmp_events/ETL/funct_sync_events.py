import logging
import azure.functions as func
from orjson import loads

from src.sync_tmp_events.ETL.sync_events_chaged import SyncronizerChagesInFact
from src.sync_tmp_events.extract.ExampleExtractInformationImpl import ExampleExtractInformationImpl
from src.sync_tmp_events.load.load_facade import LoadInformationIntoFacade
from src.sync_tmp_events.transform.TransformInformationImpl import TransformInformationImpl

route = func.Blueprint()

#sync from service bus topic trigger
@route.service_bus_topic_trigger(arg_name="azservicebus", subscription_name="eventstosync", topic_name="sync-tmp",
                               connection="ServiceBusConnListener") 
async def synceventdim(azservicebus: func.ServiceBusMessage):
    logging.info('Python ServiceBus Topic trigger processed a message: %s',
                azservicebus.get_body().decode('utf-8'))

    tmps = loads(azservicebus.get_body().decode('utf-8'))

    syncronizer = SyncronizerChagesInFact(
        extract_service=ExampleExtractInformationImpl()
        , transform_service=TransformInformationImpl()
        , load_service=LoadInformationIntoFacade()
        )

    # Act
    await syncronizer.syncronize_fact(tmps)