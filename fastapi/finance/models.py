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


class FinDistroChannel(Base):
    __tablename__ = 'fin_distro_channel'

    id = Column(Integer, primary_key=True, server_default=text("nextval('fin_distro_channel_id_seq'::regclass)"))
    chnl_cd = Column(CHAR(15))
    channel_desc = Column(CHAR(400))
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


class FinDistroChannelGroup(Base):
    __tablename__ = 'fin_distro_channel_group'

    id = Column(Integer, primary_key=True, server_default=text("nextval('fin_distro_channel_group_id_seq'::regclass)"))
    group_desc = Column(CHAR(400))
    fin_distro_channel_id = Column(Integer)
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


class FinDistroPartner(Base):
    __tablename__ = 'fin_distro_partner'

    id = Column(Integer, primary_key=True, server_default=text("nextval('fin_distro_partner_id_seq'::regclass)"))
    partner_desc = Column(CHAR(200), nullable=False)
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


class FinGlAccount(Base):
    __tablename__ = 'fin_gl_accounts'

    id = Column(Integer, primary_key=True, server_default=text("nextval('fin_gl_accounts_id_seq'::regclass)"))
    account_code = Column(String(20), nullable=False)
    account_name = Column(String(255), nullable=False)
    account_type = Column(String(50), nullable=False)
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


class GeoCityPopulation(Base):
    __tablename__ = 'geo_city_population'

    id = Column(Integer, primary_key=True, server_default=text("nextval('geo_city_population_id_seq'::regclass)"))
    city_name = Column(String(100))
    population = Column(Integer)
    country = Column(String(100), server_default=text("'USA'::character varying"))


class GeoGeography(Base):
    __tablename__ = 'geo_geography'

    id = Column(Integer, primary_key=True, server_default=text("nextval('geo_geography_id_seq'::regclass)"))
    postalcode = Column(String(10))
    country = Column(String(100))
    location_name = Column(String(100))
    msa = Column(String(100))
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


t_geo_population_by_postalcode = Table(
    'geo_population_by_postalcode', metadata,
    Column('postalcode', String(20)),
    Column('population', Integer),
    Column('country', String(100), server_default=text("'USA'::character varying"))
)


t_geo_postalcode_to_county_state = Table(
    'geo_postalcode_to_county_state', metadata,
    Column('postalcode', String(20)),
    Column('countyname', String(80)),
    Column('province', String(60)),
    Column('country', String(100), server_default=text("'USA'::character varying"))
)
