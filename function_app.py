import azure.functions as func
import logging
from src.sync_tmp_events.ETL.funct_sync_timmer import fucnt_timmer
from src.sync_tmp_events.ETL.funct_sync_events import route

app = func.FunctionApp()

app.register_functions(route)

app.register_functions(fucnt_timmer)