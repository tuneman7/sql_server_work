from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select
from typing import List
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from connector import *
from models import *

Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Create
@app.post("/fin_account_activity/")
def create_fin_account_activity(fin_account_activity: dict, db: Session = Depends(get_db)):
    db_fin_account_activity = FinAccountActivity(**fin_account_activity)
    db.add(db_fin_account_activity)
    db.commit()
    db.refresh(db_fin_account_activity)
    return db_fin_account_activity

# Read
@app.get("/fin_account_activity/{id}")
def read_fin_account_activity(id: int, db: Session = Depends(get_db)):
    fin_account_activity = db.query(FinAccountActivity).filter(FinAccountActivity.id == id).first()
    if fin_account_activity is None:
        raise HTTPException(status_code=404, detail="FinAccountActivity not found")
    return fin_account_activity

# Update
@app.put("/fin_account_activity/{id}")
def update_fin_account_activity(id: int, fin_account_activity: dict, db: Session = Depends(get_db)):
    db_fin_account_activity = db.query(FinAccountActivity).filter(FinAccountActivity.id == id).first()
    if db_fin_account_activity is None:
        raise HTTPException(status_code=404, detail="FinAccountActivity not found")

    for key, value in fin_account_activity.items():
        setattr(db_fin_account_activity, key, value)

    db.commit()
    db.refresh(db_fin_account_activity)
    return db_fin_account_activity

# Delete
@app.delete("/fin_account_activity/{id}")
def delete_fin_account_activity(id: int, db: Session = Depends(get_db)):
    fin_account_activity = db.query(FinAccountActivity).filter(FinAccountActivity.id == id).first()
    if fin_account_activity is None:
        raise HTTPException(status_code=404, detail="FinAccountActivity not found")

    db.delete(fin_account_activity)
    db.commit()
    return fin_account_activity

# List
@app.get("/fin_account_activity/")
def list_fin_account_activities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fin_account_activities = db.query(FinAccountActivity).offset(skip).limit(limit).all()
    return fin_account_activities



# Create
@app.post("/fin_distro_channel_group/")
def create_fin_distro_channel_group(fin_distro_channel_group: dict, db: Session = Depends(get_db)):
    db_fin_distro_channel_group = FinDistroChannelGroup(**fin_distro_channel_group)
    db.add(db_fin_distro_channel_group)
    db.commit()
    db.refresh(db_fin_distro_channel_group)
    return db_fin_distro_channel_group

# Read
@app.get("/fin_distro_channel_group/{id}")
def read_fin_distro_channel_group(id: int, db: Session = Depends(get_db)):
    fin_distro_channel_group = db.query(FinDistroChannelGroup).filter(FinDistroChannelGroup.id == id).first()
    if fin_distro_channel_group is None:
        raise HTTPException(status_code=404, detail="FinDistroChannelGroup not found")
    return fin_distro_channel_group

# Update
@app.put("/fin_distro_channel_group/{id}")
def update_fin_distro_channel_group(id: int, fin_distro_channel_group: dict, db: Session = Depends(get_db)):
    db_fin_distro_channel_group = db.query(FinDistroChannelGroup).filter(FinDistroChannelGroup.id == id).first()
    if db_fin_distro_channel_group is None:
        raise HTTPException(status_code=404, detail="FinDistroChannelGroup not found")

    for key, value in fin_distro_channel_group.items():
        setattr(db_fin_distro_channel_group, key, value)

    db.commit()
    db.refresh(db_fin_distro_channel_group)
    return db_fin_distro_channel_group

# Delete
@app.delete("/fin_distro_channel_group/{id}")
def delete_fin_distro_channel_group(id: int, db: Session = Depends(get_db)):
    fin_distro_channel_group = db.query(FinDistroChannelGroup).filter(FinDistroChannelGroup.id == id).first()
    if fin_distro_channel_group is None:
        raise HTTPException(status_code=404, detail="FinDistroChannelGroup not found")

    db.delete(fin_distro_channel_group)
    db.commit()
    return fin_distro_channel_group

# List
@app.get("/fin_distro_channel_group/")
def list_fin_distro_channel_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fin_distro_channel_groups = db.query(FinDistroChannelGroup).offset(skip).limit(limit).all()
    return fin_distro_channel_groups

# Create
@app.post("/fin_distro_channel/")
def create_fin_distro_channel(fin_distro_channel: dict, db: Session = Depends(get_db)):
    db_fin_distro_channel = FinDistroChannel(**fin_distro_channel)
    db.add(db_fin_distro_channel)
    db.commit()
    db.refresh(db_fin_distro_channel)
    return db_fin_distro_channel

# Read
@app.get("/fin_distro_channel/{id}")
def read_fin_distro_channel(id: int, db: Session = Depends(get_db)):
    fin_distro_channel = db.query(FinDistroChannel).filter(FinDistroChannel.id == id).first()
    if fin_distro_channel is None:
        raise HTTPException(status_code=404, detail="FinDistroChannel not found")
    return fin_distro_channel

# Update
@app.put("/fin_distro_channel/{id}")
def update_fin_distro_channel(id: int, fin_distro_channel: dict, db: Session = Depends(get_db)):
    db_fin_distro_channel = db.query(FinDistroChannel).filter(FinDistroChannel.id == id).first()
    if db_fin_distro_channel is None:
        raise HTTPException(status_code=404, detail="FinDistroChannel not found")

    for key, value in fin_distro_channel.items():
        setattr(db_fin_distro_channel, key, value)

    db.commit()
    db.refresh(db_fin_distro_channel)
    return db_fin_distro_channel

# Delete
@app.delete("/fin_distro_channel/{id}")
def delete_fin_distro_channel(id: int, db: Session = Depends(get_db)):
    fin_distro_channel = db.query(FinDistroChannel).filter(FinDistroChannel.id == id).first()
    if fin_distro_channel is None:
        raise HTTPException(status_code=404, detail="FinDistroChannel not found")

    db.delete(fin_distro_channel)
    db.commit()
    return fin_distro_channel

# List
@app.get("/fin_distro_channel/")
def list_fin_distro_channels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fin_distro_channels = db.query(FinDistroChannel).offset(skip).limit(limit).all()
    return fin_distro_channels


# Create
@app.post("/fin_distro_partner/")
def create_fin_distro_partner(fin_distro_partner: dict, db: Session = Depends(get_db)):
    db_fin_distro_partner = FinDistroPartner(**fin_distro_partner)
    db.add(db_fin_distro_partner)
    db.commit()
    db.refresh(db_fin_distro_partner)
    return db_fin_distro_partner

# Read
@app.get("/fin_distro_partner/{id}")
def read_fin_distro_partner(id: int, db: Session = Depends(get_db)):
    fin_distro_partner = db.query(FinDistroPartner).filter(FinDistroPartner.id == id).first()
    if fin_distro_partner is None:
        raise HTTPException(status_code=404, detail="FinDistroPartner not found")
    return fin_distro_partner

# Update
@app.put("/fin_distro_partner/{id}")
def update_fin_distro_partner(id: int, fin_distro_partner: dict, db: Session = Depends(get_db)):
    db_fin_distro_partner = db.query(FinDistroPartner).filter(FinDistroPartner.id == id).first()
    if db_fin_distro_partner is None:
        raise HTTPException(status_code=404, detail="FinDistroPartner not found")

    for key, value in fin_distro_partner.items():
        setattr(db_fin_distro_partner, key, value)

    db.commit()
    db.refresh(db_fin_distro_partner)
    return db_fin_distro_partner

# Delete
@app.delete("/fin_distro_partner/{id}")
def delete_fin_distro_partner(id: int, db: Session = Depends(get_db)):
    fin_distro_partner = db.query(FinDistroPartner).filter(FinDistroPartner.id == id).first()
    if fin_distro_partner is None:
        raise HTTPException(status_code=404, detail="FinDistroPartner not found")

    db.delete(fin_distro_partner)
    db.commit()
    return fin_distro_partner

# List
@app.get("/fin_distro_partner/")
def list_fin_distro_partners(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fin_distro_partners = db.query(FinDistroPartner).offset(skip).limit(limit).all()
    return fin_distro_partners


# Create
@app.post("/fin_gl_accounts/")
def create_fin_gl_account(fin_gl_account: dict, db: Session = Depends(get_db)):
    db_fin_gl_account = FinGlAccount(**fin_gl_account)
    db.add(db_fin_gl_account)
    db.commit()
    db.refresh(db_fin_gl_account)
    return db_fin_gl_account

# Read
@app.get("/fin_gl_accounts/{id}")
def read_fin_gl_account(id: int, db: Session = Depends(get_db)):
    fin_gl_account = db.query(FinGlAccount).filter(FinGlAccount.id == id).first()
    if fin_gl_account is None:
        raise HTTPException(status_code=404, detail="FinGlAccount not found")
    return fin_gl_account

# Update
@app.put("/fin_gl_accounts/{id}")
def update_fin_gl_account(id: int, fin_gl_account: dict, db: Session = Depends(get_db)):
    db_fin_gl_account = db.query(FinGlAccount).filter(FinGlAccount.id == id).first()
    if db_fin_gl_account is None:
        raise HTTPException(status_code=404, detail="FinGlAccount not found")

    for key, value in fin_gl_account.items():
        setattr(db_fin_gl_account, key, value)

    db.commit()
    db.refresh(db_fin_gl_account)
    return db_fin_gl_account

# Delete
@app.delete("/fin_gl_accounts/{id}")
def delete_fin_gl_account(id: int, db: Session = Depends(get_db)):
    fin_gl_account = db.query(FinGlAccount).filter(FinGlAccount.id == id).first()
    if fin_gl_account is None:
        raise HTTPException(status_code=404, detail="FinGlAccount not found")

    db.delete(fin_gl_account)
    db.commit()
    return fin_gl_account

# List
@app.get("/fin_gl_accounts/")
def list_fin_gl_accounts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fin_gl_accounts = db.query(FinGlAccount).offset(skip).limit(limit).all()
    return fin_gl_accounts


@app.post("/geo_city_population/")
def create_geo_city_population(geo_city_population: dict, db: Session = Depends(get_db)):
    db_geo_city_population = GeoCityPopulation(**geo_city_population)
    db.add(db_geo_city_population)
    db.commit()
    db.refresh(db_geo_city_population)
    return db_geo_city_population

# Read
@app.get("/geo_city_population/{id}")
def read_geo_city_population(id: int, db: Session = Depends(get_db)):
    geo_city_population = db.query(GeoCityPopulation).filter(GeoCityPopulation.id == id).first()
    if geo_city_population is None:
        raise HTTPException(status_code=404, detail="GeoCityPopulation not found")
    return geo_city_population

# Update
@app.put("/geo_city_population/{id}")
def update_geo_city_population(id: int, geo_city_population: dict, db: Session = Depends(get_db)):
    db_geo_city_population = db.query(GeoCityPopulation).filter(GeoCityPopulation.id == id).first()
    if db_geo_city_population is None:
        raise HTTPException(status_code=404, detail="GeoCityPopulation not found")

    for key, value in geo_city_population.items():
        setattr(db_geo_city_population, key, value)

    db.commit()
    db.refresh(db_geo_city_population)
    return db_geo_city_population

# Delete
@app.delete("/geo_city_population/{id}")
def delete_geo_city_population(id: int, db: Session = Depends(get_db)):
    geo_city_population = db.query(GeoCityPopulation).filter(GeoCityPopulation.id == id).first()
    if geo_city_population is None:
        raise HTTPException(status_code=404, detail="GeoCityPopulation not found")

    db.delete(geo_city_population)
    db.commit()
    return geo_city_population

# List
@app.get("/geo_city_population/")
def list_geo_city_population(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    geo_city_populations = db.query(GeoCityPopulation).offset(skip).limit(limit).all()
    return geo_city_populations



# Create
@app.post("/geo_geography/")
def create_geo_geography(geo_geography: dict, db: Session = Depends(get_db)):
    db_geo_geography = GeoGeography(**geo_geography)
    db.add(db_geo_geography)
    db.commit()
    db.refresh(db_geo_geography)
    return db_geo_geography

# Read
@app.get("/geo_geography/{id}")
def read_geo_geography(id: int, db: Session = Depends(get_db)):
    geo_geography = db.query(GeoGeography).filter(GeoGeography.id == id).first()
    if geo_geography is None:
        raise HTTPException(status_code=404, detail="GeoGeography not found")
    return geo_geography

# Update
@app.put("/geo_geography/{id}")
def update_geo_geography(id: int, geo_geography: dict, db: Session = Depends(get_db)):
    db_geo_geography = db.query(GeoGeography).filter(GeoGeography.id == id).first()
    if db_geo_geography is None:
        raise HTTPException(status_code=404, detail="GeoGeography not found")

    for key, value in geo_geography.items():
        setattr(db_geo_geography, key, value)

    db.commit()
    db.refresh(db_geo_geography)
    return db_geo_geography

# Delete
@app.delete("/geo_geography/{id}")
def delete_geo_geography(id: int, db: Session = Depends(get_db)):
    geo_geography = db.query(GeoGeography).filter(GeoGeography.id == id).first()
    if geo_geography is None:
        raise HTTPException(status_code=404, detail="GeoGeography not found")

    db.delete(geo_geography)
    db.commit()
    return geo_geography

# List
@app.get("/geo_geography/")
def list_geo_geography(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    geo_geographies = db.query(GeoGeography).offset(skip).limit(limit).all()
    return geo_geographies


# Create
@app.post("/geo_population_by_postalcode/")
def create_geo_population(geo_data: dict, db: Session = Depends(get_db)):
    insert_stmt = t_geo_population_by_postalcode.insert().values(**geo_data)
    db.execute(insert_stmt)
    db.commit()
    return geo_data

# Read
@app.get("/geo_population_by_postalcode/{postalcode}")
def read_geo_population(postalcode: str, db: Session = Depends(get_db)):
    select_stmt = select([t_geo_population_by_postalcode]).where(t_geo_population_by_postalcode.c.postalcode == postalcode)
    result = db.execute(select_stmt).first()
    if result is None:
        raise HTTPException(status_code=404, detail="GeoPopulationByPostalcode not found")
    return dict(result)

# Update
@app.put("/geo_population_by_postalcode/{postalcode}")
def update_geo_population(postalcode: str, geo_data: dict, db: Session = Depends(get_db)):
    update_stmt = t_geo_population_by_postalcode.update().where(t_geo_population_by_postalcode.c.postalcode == postalcode).values(**geo_data)
    result = db.execute(update_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="GeoPopulationByPostalcode not found")
    db.commit()
    return geo_data

# Delete
@app.delete("/geo_population_by_postalcode/{postalcode}")
def delete_geo_population(postalcode: str, db: Session = Depends(get_db)):
    delete_stmt = t_geo_population_by_postalcode.delete().where(t_geo_population_by_postalcode.c.postalcode == postalcode)
    result = db.execute(delete_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="GeoPopulationByPostalcode not found")
    db.commit()
    return {"message": "GeoPopulationByPostalcode deleted"}

# List
@app.get("/geo_population_by_postalcode/")
def list_geo_population(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    select_stmt = select([t_geo_population_by_postalcode]).offset(skip).limit(limit)
    result = db.execute(select_stmt).fetchall()
    return [dict(row) for row in result]

# Create
@app.post("/geo_postalcode_to_county_state/")
def create_geo_postalcode(data: dict, db: Session = Depends(get_db)):
    insert_stmt = t_geo_postalcode_to_county_state.insert().values(**data)
    db.execute(insert_stmt)
    db.commit()
    return data

# Read
@app.get("/geo_postalcode_to_county_state/{postalcode}")
def read_geo_postalcode(postalcode: str, db: Session = Depends(get_db)):
    select_stmt = select([t_geo_postalcode_to_county_state]).where(t_geo_postalcode_to_county_state.c.postalcode == postalcode)
    result = db.execute(select_stmt).first()
    if result is None:
        raise HTTPException(status_code=404, detail="GeoPostalcodeToCountyState not found")
    return dict(result)

# Update
@app.put("/geo_postalcode_to_county_state/{postalcode}")
def update_geo_postalcode(postalcode: str, data: dict, db: Session = Depends(get_db)):
    update_stmt = t_geo_postalcode_to_county_state.update().where(t_geo_postalcode_to_county_state.c.postalcode == postalcode).values(**data)
    result = db.execute(update_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="GeoPostalcodeToCountyState not found")
    db.commit()
    return data

# Delete
@app.delete("/geo_postalcode_to_county_state/{postalcode}")
def delete_geo_postalcode(postalcode: str, db: Session = Depends(get_db)):
    delete_stmt = t_geo_postalcode_to_county_state.delete().where(t_geo_postalcode_to_county_state.c.postalcode == postalcode)
    result = db.execute(delete_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="GeoPostalcodeToCountyState not found")
    db.commit()
    return {"message": "GeoPostalcodeToCountyState deleted"}

# List
@app.get("/geo_postalcode_to_county_state/")
def list_geo_postalcode(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    select_stmt = select([t_geo_postalcode_to_county_state]).offset(skip).limit(limit)
    result = db.execute(select_stmt).fetchall()
    return [dict(row) for row in result]
