# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Integer, String, Table, text
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FinAccountActivity(Base):
    __tablename__ = 'fin_account_activity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('fin_account_activity_id_seq'::regclass)"))
    product_id = Column(Integer, nullable=False)
    customer_id = Column(Integer)
    account_id = Column(Integer, nullable=False)
    post_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    amt_usd = Column(MONEY)
    geo_geography_id = Column(Integer)
    fin_distro_channel_id = Column(Integer)
    fin_distro_partner_id = Column(Integer)
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


