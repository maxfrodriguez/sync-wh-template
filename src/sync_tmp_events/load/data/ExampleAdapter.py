from datetime import datetime

from src.sync_tmp_events.load.data.SAFactExample import SAFactExample



class ExampleAdapter(SAFactExample):
    def __init__(self, **kwargs):
        if kwargs["id"] == -1:
            kwargs["id"] = None
        del kwargs["hash"]
        del kwargs["de_ship_seq"]
        del kwargs["ev_de_appointment"]
        del kwargs["created_at_str"]
        del kwargs["updated_at_str"]
        del kwargs["schedule_date_str"]
        super().__init__(**kwargs)