# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Integer, String, Table, text
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class GeoCityPopulation(Base):
    __tablename__ = 'geo_city_population'

    id = Column(Integer, primary_key=True, server_default=text("nextval('geo_city_population_id_seq'::regclass)"))
    city_name = Column(String(100))
    population = Column(Integer)
    country = Column(String(100), server_default=text("'USA'::character varying"))


