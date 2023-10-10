# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Integer, String, Table, text
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class FinDistroChannelGroup(Base):
    __tablename__ = 'fin_distro_channel_group'

    id = Column(Integer, primary_key=True, server_default=text("nextval('fin_distro_channel_group_id_seq'::regclass)"))
    group_desc = Column(CHAR(400))
    fin_distro_channel_id = Column(Integer)
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


