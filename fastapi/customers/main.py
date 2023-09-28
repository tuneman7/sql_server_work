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

# Create a CustomerInfo entry
@app.post("/customer_info/")
def create_customer_info(customer_info: CustomerInfo, db: Session = Depends(get_db)):
    db.add(customer_info)
    db.commit()
    db.refresh(customer_info)
    return customer_info

# Retrieve a CustomerInfo entry by ID
@app.get("/customer_info/{customer_info_id}/")
def read_customer_info(customer_info_id: int, db: Session = Depends(get_db)):
    customer_info = db.query(CustomerInfo).filter(CustomerInfo.id == customer_info_id).first()
    if customer_info is None:
        raise HTTPException(status_code=404, detail="CustomerInfo not found")
    return customer_info

# Retrieve all CustomerInfo entries
@app.get("/customer_info/")
def read_customer_infos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customer_infos = db.query(CustomerInfo).offset(skip).limit(limit).all()
    return customer_infos

# Update a CustomerInfo entry by ID
@app.put("/customer_info/{customer_info_id}/")
def update_customer_info(customer_info_id: int, customer_info: CustomerInfo, db: Session = Depends(get_db)):
    db_customer_info = db.query(CustomerInfo).filter(CustomerInfo.id == customer_info_id).first()
    if db_customer_info is None:
        raise HTTPException(status_code=404, detail="CustomerInfo not found")
    
    db_customer_info.f_name = customer_info.f_name
    db_customer_info.l_name = customer_info.l_name
    db_customer_info.email_address = customer_info.email_address
    db_customer_info.country = customer_info.country
    db_customer_info.postalcode = customer_info.postalcode
    db_customer_info.city_name = customer_info.city_name
    db_customer_info.province = customer_info.province
    db.commit()
    db.refresh(db_customer_info)
    return db_customer_info

# Delete a CustomerInfo entry by ID
@app.delete("/customer_info/{customer_info_id}/")
def delete_customer_info(customer_info_id: int, db: Session = Depends(get_db)):
    customer_info = db.query(CustomerInfo).filter(CustomerInfo.id == customer_info_id).first()
    if customer_info is None:
        raise HTTPException(status_code=404, detail="CustomerInfo not found")
    
    db.delete(customer_info)
    db.commit()
    return customer_info
