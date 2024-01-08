from typing import Final

EXAMPLE_EXTRACT_QUERY: Final[
    str
] = """
 SELECT
    ds.ds_id
    , ev.de_id
    , ev.de_ship_seq
    , ev.de_appointment AS schedule_date
    , ev.de_arrival AS arrival_date
    , ev.de_driver AS driver_id
    , MAX(ds_snap.id) as ds_id_snapshot
    , MAX(ev_snap.id) as de_id_snapshot
FROM dim_ontime_delivery dod
INNER JOIN fact_shipments ds ON ds.ds_id = dod.ds_id
INNER JOIN shipments ds_snap on ds_snap.ds_id = ds.ds_id
LEFT JOIN fact_events ev ON ev.de_id = dod.de_id_client
LEFT JOIN events ev_snap on ev_snap.de_id = ev.de_id
LEFT JOIN view_wonderful_duplicate_not_shipment won on won.ds_id = ds.ds_id
WHERE
  ds.ds_status IN ('K', 'N', 'Q', 'T', 'W')
  AND 
  ev.de_appointment BETWEEN '{start_dt}' AND '{end_dt}'
  AND
  won.ds_id is null
GROUP BY
    ds.ds_id
    , ev.de_id
    , ev.de_ship_seq
    , ev.de_appointment
    , ev.de_arrival
    , ev.de_driver
ORDER BY
ev.de_appointment ASC
"""

EXAMPLE_UPDATE_QUERY: Final[str] = """
    SELECT
        sch.id
        , sch.ds_id
        , sch.de_id
        , FORMAT(sch.schedule_date, 'yyyy-MM-dd HH:mm:ss') AS schedule_date_str
        , ev.de_appointment as ev_de_appointment
        , ev.de_arrival AS arrival_date
        , ev.de_driver AS driver_id
        , FORMAT(sch.created_at, 'yyyy-MM-dd HH:mm:ss') AS created_at_str
        , sch.ds_id_snapshot
        , sch.de_id_snapshot
    FROM fact_scheduled_vs_completed sch
    LEFT JOIN fact_events ev ON ev.de_id = sch.de_id
    WHERE
    ev.de_id in ({de_ids})
    ORDER BY
    ev.de_appointment ASC
"""