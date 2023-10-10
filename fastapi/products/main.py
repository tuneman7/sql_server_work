from fastapi import FastAPI, HTTPException, Depends
from json import JSONEncoder
import json
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc
from sqlalchemy.sql import select
from typing import List
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from connector import *
from models import *

Base.metadata.create_all(bind=engine)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)

# FastAPI app
app = FastAPI()

@app.get("/product_types/")
def get_all_product_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_types = db.query(ProductType).order_by(desc(ProductType.id)).offset(skip).limit(limit).all()
    return product_types

# Create a ProductType entry using a dictionary as input
@app.post("/product_type/")
def create_product_type(product_type_data: dict, db: Session = Depends(get_db)):
    create_dt = datetime.now()
    created_by = "YourUser"  # Set the appropriate user here

    # Add created_by and create_dt to the input dictionary
    product_type_data["created_by"] = created_by
    product_type_data["create_dt"] = create_dt

    # Create the ProductType object using the input dictionary
    product_type = ProductType(**product_type_data)

    # Add to the database and commit
    db.add(product_type)
    db.commit()
    db.refresh(product_type)
    return product_type

# Update a ProductType by ID using a dictionary as input
@app.put("/product_type/{product_type_id}")
def update_product_type(product_type_id: int, product_type_data: dict, db: Session = Depends(get_db)):
    update_dt = datetime.now()
    updated_by = "YourUser"  # Set the appropriate user here

    # Get the ProductType by ID
    product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="ProductType not found")

    # Update the ProductType attributes using the input dictionary
    product_type.updated_by = updated_by
    product_type.update_dt = update_dt
    for key, value in product_type_data.items():
        setattr(product_type, key, value)

    # Commit the changes
    db.commit()
    db.refresh(product_type)

    return product_type

# Get a ProductType by ID
@app.get("/product_type/{product_type_id}")
def get_product_type(product_type_id: int, db: Session = Depends(get_db)):
    product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="ProductType not found")
    
    return product_type

# Delete a ProductType by ID
@app.delete("/product_type/{product_type_id}")
def delete_product_type(product_type_id: int, db: Session = Depends(get_db)):
    product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if not product_type:
        raise HTTPException(status_code=404, detail="ProductType not found")

    # Delete the ProductType and commit
    db.delete(product_type)
    db.commit()

    return {"message": "ProductType deleted"}

# Create a Product entry using a dictionary as input
@app.post("/products/")
def create_product(product_data: dict, db: Session = Depends(get_db)):
    create_dt = datetime.now()
    created_by = "YourUser"  # Set the appropriate user here

    # Add created_by and create_dt to the input dictionary
    product_data["created_by"] = created_by
    product_data["created_dt"] = create_dt

    # Create the Product object using the input dictionary
    product = Products(**product_data)

    # Add to the database and commit
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# Update a Product by ID using a dictionary as input
@app.put("/products/{product_id}")
def update_product(product_id: int, product_data: dict, db: Session = Depends(get_db)):
    update_dt = datetime.now()
    updated_by = "YourUser"  # Set the appropriate user here

    # Get the Product by ID
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the Product attributes using the input dictionary
    product.updated_by = updated_by
    product.updated_dt = update_dt
    for key, value in product_data.items():
        setattr(product, key, value)

    # Commit the changes
    db.commit()
    db.refresh(product)
    return product

# Get a Product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

# Delete a Product by ID
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delete the Product and commit
    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}

# Create a ProductPrice entry using a dictionary as input
@app.post("/product_prices/")
def create_product_price(product_price_data: dict, db: Session = Depends(get_db)):
    create_dt = datetime.now()
    created_by = "YourUser"  # Set the appropriate user here

    # Add created_by and create_dt to the input dictionary
    product_price_data["created_by"] = created_by
    product_price_data["created_dt"] = create_dt

    # Create the ProductPrice object using the input dictionary
    product_price = ProductPrice(**product_price_data)

    # Add to the database and commit
    db.add(product_price)
    db.commit()

    return product_price

# Update a ProductPrice by ID using a dictionary as input
@app.put("/product_prices/{product_price_id}")
def update_product_price(product_price_id: int, product_price_data: dict, db: Session = Depends(get_db)):
    update_dt = datetime.now()
    updated_by = "YourUser"  # Set the appropriate user here

    # Get the ProductPrice by ID
    product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if not product_price:
        raise HTTPException(status_code=404, detail="ProductPrice not found")

    # Update the ProductPrice attributes using the input dictionary
    product_price.updated_by = updated_by
    product_price.updated_dt = update_dt
    for key, value in product_price_data.items():
        setattr(product_price, key, value)

    # Commit the changes
    db.commit()

    return product_price

# Get a ProductPrice by ID
@app.get("/product_prices/{product_price_id}")
def get_product_price(product_price_id: int, db: Session = Depends(get_db)):
    product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if not product_price:
        raise HTTPException(status_code=404, detail="ProductPrice not found")

    return product_price

# Delete a ProductPrice by ID
@app.delete("/product_prices/{product_price_id}")
def delete_product_price(product_price_id: int, db: Session = Depends(get_db)):
    product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if not product_price:
        raise HTTPException(status_code=404, detail="ProductPrice not found")

    # Delete the ProductPrice and commit
    db.delete(product_price)
    db.commit()

    return {"message": "ProductPrice deleted"}

# Create a ProductPriceHistory entry using a dictionary as input
@app.post("/product_price_history/")
def create_product_price_history(product_price_history_data: dict, db: Session = Depends(get_db)):
    create_dt = datetime.now()
    created_by = "YourUser"  # Set the appropriate user here

    # Add created_by and create_dt to the input dictionary
    product_price_history_data["created_by"] = created_by
    product_price_history_data["created_dt"] = create_dt

    # Create the ProductPriceHistory object using the input dictionary
    product_price_history = ProductPriceHistory(**product_price_history_data)

    # Add to the database and commit
    db.add(product_price_history)
    db.commit()

    return product_price_history

# Update a ProductPriceHistory by ID using a dictionary as input
@app.put("/product_price_history/{product_price_history_id}")
def update_product_price_history(product_price_history_id: int, product_price_history_data: dict, db: Session = Depends(get_db)):
    update_dt = datetime.now()
    updated_by = "YourUser"  # Set the appropriate user here

    # Get the ProductPriceHistory by ID
    product_price_history = db.query(ProductPriceHistory).filter(ProductPriceHistory.id == product_price_history_id).first()
    if not product_price_history:
        raise HTTPException(status_code=404, detail="ProductPriceHistory not found")

    # Update the ProductPriceHistory attributes using the input dictionary
    product_price_history.updated_by = updated_by
    product_price_history.updated_dt = update_dt
    for key, value in product_price_history_data.items():
        setattr(product_price_history, key, value)

    # Commit the changes
    db.commit()

    return product_price_history

# Get a ProductPriceHistory by ID
@app.get("/product_price_history/{product_price_history_id}")
def get_product_price_history(product_price_history_id: int, db: Session = Depends(get_db)):
    product_price_history = db.query(ProductPriceHistory).filter(ProductPriceHistory.id == product_price_history_id).first()
    if not product_price_history:
        raise HTTPException(status_code=404, detail="ProductPriceHistory not found")

    return product_price_history

# Delete a ProductPriceHistory by ID
@app.delete("/product_price_history/{product_price_history_id}")
def delete_product_price_history(product_price_history_id: int, db: Session = Depends(get_db)):
    product_price_history = db.query(ProductPriceHistory).filter(ProductPriceHistory.id == product_price_history_id).first()
    if not product_price_history:
        raise HTTPException(status_code=404, detail="ProductPriceHistory not found")

    # Delete the ProductPriceHistory and commit
    db.delete(product_price_history)
    db.commit()

    return {"message": "ProductPriceHistory deleted"}

