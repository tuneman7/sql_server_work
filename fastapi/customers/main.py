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

# Get all CustomerInfo entries
@app.get("/customer_info/")
def get_all_customer_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customer_info = db.query(CustomerInfo).offset(skip).limit(limit).all()
    return customer_info

# Get a CustomerInfo entry by ID
@app.get("/customer_info/{customer_info_id}")
def get_customer_info(customer_info_id: int, db: Session = Depends(get_db)):
    customer_info = db.query(CustomerInfo).filter(CustomerInfo.id == customer_info_id).first()
    if not customer_info:
        raise HTTPException(status_code=404, detail="CustomerInfo not found")
    
    return customer_info

# Update a CustomerInfo entry by ID using a dictionary as input
@app.put("/customer_info/{customer_info_id}")
def update_customer_info(customer_info_id: int, customer_info_data: dict, db: Session = Depends(get_db)):
    update_dt = datetime.now()
    updated_by = "YourUser"  # Set the appropriate user here

    # Get the CustomerInfo by ID
    customer_info = db.query(CustomerInfo).filter(CustomerInfo.id == customer_info_id).first()
    if not customer_info:
        raise HTTPException(status_code=404, detail="CustomerInfo not found")

    # Update the CustomerInfo attributes using the input dictionary
    customer_info.updated_by = updated_by
    customer_info.updated_dt = update_dt
    for key, value in customer_info_data.items():
        setattr(customer_info, key, value)

    # Commit the changes
    db.commit()
    db.refresh(customer_info)

    return customer_info

# Delete a CustomerInfo entry by ID
@app.delete("/customer_info/{customer_info_id}")
def delete_customer_info(customer_info_id: int, db: Session = Depends(get_db)):
    customer_info = db.query(CustomerInfo).filter(CustomerInfo.id == customer_info_id).first()
    if not customer_info:
        raise HTTPException(status_code=404, detail="CustomerInfo not found")

    # Delete the CustomerInfo and commit
    db.delete(customer_info)
    db.commit()

    return {"message": "CustomerInfo deleted"}



# Create a CustomerProduct entry using a dictionary as input
@app.post("/customer_product/")
def create_customer_product(customer_product_data: dict, db: Session = Depends(get_db)):
    create_dt = datetime.now()
    created_by = "YourUser"  # Set the appropriate user here

    # Add created_by and create_dt to the input dictionary
    customer_product_data["created_by"] = created_by
    customer_product_data["created_dt"] = create_dt

    # Create the CustomerProduct object using the input dictionary
    customer_product = CustomerProduct(**customer_product_data)

    # Add to the database and commit
    db.add(customer_product)
    db.commit()
    db.refresh(customer_product)
    return customer_product

# Get all CustomerProduct entries
@app.get("/customer_product/")
def get_all_customer_product(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customer_product = db.query(CustomerProduct).offset(skip).limit(limit).all()
    return customer_product

# Get a CustomerProduct entry by ID
@app.get("/customer_product/{customer_product_id}")
def get_customer_product(customer_product_id: int, db: Session = Depends(get_db)):
    customer_product = db.query(CustomerProduct).filter(CustomerProduct.id == customer_product_id).first()
    if not customer_product:
        raise HTTPException(status_code=404, detail="CustomerProduct not found")
    
    return customer_product

# Update a CustomerProduct entry by ID using a dictionary as input
@app.put("/customer_product/{customer_product_id}")
def update_customer_product(customer_product_id: int, customer_product_data: dict, db: Session = Depends(get_db)):
    update_dt = datetime.now()
    updated_by = "YourUser"  # Set the appropriate user here

    # Get the CustomerProduct by ID
    customer_product = db.query(CustomerProduct).filter(CustomerProduct.id == customer_product_id).first()
    if not customer_product:
        raise HTTPException(status_code=404, detail="CustomerProduct not found")

    # Update the CustomerProduct attributes using the input dictionary
    customer_product.updated_by = updated_by
    customer_product.updated_dt = update_dt
    for key, value in customer_product_data.items():
        setattr(customer_product, key, value)

    # Commit the changes
    db.commit()
    db.refresh(customer_product)

    return customer_product

# Delete a CustomerProduct entry by ID
@app.delete("/customer_product/{customer_product_id}")
def delete_customer_product(customer_product_id: int, db: Session = Depends(get_db)):
    customer_product = db.query(CustomerProduct).filter(CustomerProduct.id == customer_product_id).first()
    if not customer_product:
        raise HTTPException(status_code=404, detail="CustomerProduct not found")

    # Delete the CustomerProduct and commit
    db.delete(customer_product)
    db.commit()

    return {"message": "CustomerProduct deleted"}


# Create a CustomerProductHistory entry using a dictionary as input
@app.post("/customer_product_history/")
def create_customer_product_history(customer_product_history_data: dict, db: Session = Depends(get_db)):
    create_dt = datetime.now()
    created_by = "YourUser"  # Set the appropriate user here

    # Add created_by and create_dt to the input dictionary
    customer_product_history_data["created_by"] = created_by
    customer_product_history_data["created_dt"] = create_dt

    # Create the CustomerProductHistory object using the input dictionary
    customer_product_history = CustomerProductHistory(**customer_product_history_data)

    # Add to the database and commit
    db.add(customer_product_history)
    db.commit()
    db.refresh(customer_product_history)
    return customer_product_history

# Get all CustomerProductHistory entries
@app.get("/customer_product_history/")
def get_all_customer_product_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customer_product_history = db.query(CustomerProductHistory).offset(skip).limit(limit).all()
    return customer_product_history

# Get a CustomerProductHistory entry by ID
@app.get("/customer_product_history/{customer_product_history_id}")
def get_customer_product_history(customer_product_history_id: int, db: Session = Depends(get_db)):
    customer_product_history = db.query(CustomerProductHistory).filter(CustomerProductHistory.id == customer_product_history_id).first()
    if not customer_product_history:
        raise HTTPException(status_code=404, detail="CustomerProductHistory not found")
    
    return customer_product_history

# Update a CustomerProductHistory entry by ID using a dictionary as input
@app.put("/customer_product_history/{customer_product_history_id}")
def update_customer_product_history(customer_product_history_id: int, customer_product_history_data: dict, db: Session = Depends(get_db)):
    update_dt = datetime.now()
    updated_by = "YourUser"  # Set the appropriate user here

    # Get the CustomerProductHistory by ID
    customer_product_history = db.query(CustomerProductHistory).filter(CustomerProductHistory.id == customer_product_history_id).first()
    if not customer_product_history:
        raise HTTPException(status_code=404, detail="CustomerProductHistory not found")

    # Update the CustomerProductHistory attributes using the input dictionary
    customer_product_history.updated_by = updated_by
    customer_product_history.updated_dt = update_dt
    for key, value in customer_product_history_data.items():
        setattr(customer_product_history, key, value)

    # Commit the changes
    db.commit()
    db.refresh(customer_product_history)

    return customer_product_history

# Delete a CustomerProductHistory entry by ID
@app.delete("/customer_product_history/{customer_product_history_id}")
def delete_customer_product_history(customer_product_history_id: int, db: Session = Depends(get_db)):
    customer_product_history = db.query(CustomerProductHistory).filter(CustomerProductHistory.id == customer_product_history_id).first()
    if not customer_product_history:
        raise HTTPException(status_code=404, detail="CustomerProductHistory not found")

    # Delete the CustomerProductHistory and commit
    db.delete(customer_product_history)
    db.commit()

    return {"message": "CustomerProductHistory deleted"}

