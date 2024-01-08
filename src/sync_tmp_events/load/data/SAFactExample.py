from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Time,
    desc,
    select,
)

from common.common_infrastructure.dataaccess.db_ware_house_access.base_model import SAModelBaseWareHouse
from common.common_infrastructure.dataaccess.db_ware_house_access.sa_models_whdb import Base


class SAFactExample(Base, SAModelBaseWareHouse):
    __tablename__ = "fact_scheduled_vs_completed"

    ds_id = Column(Integer, nullable=True)
    de_id = Column(Integer, nullable=True)
    schedule_date = Column(DateTime, nullable=True)
    arrival_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=True)
    driver_id = Column(Integer, nullable=True)
    ds_id_snapshot = Column(Integer, nullable=True)
    de_id_snapshot = Column(Integer, nullable=True)

    #hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime, nullable=False)

    #shipment = relationship("SAShipment", uselist=False, back_populates="events")
    # stops = relationship("SAStops", uselist=False, back_populates="event")