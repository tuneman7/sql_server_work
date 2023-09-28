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

# Create a ProductType entry
@app.post("/product_type/")
def create_product_type(product_type: ProductType, db: Session = Depends(get_db)):
    db.add(product_type)
    db.commit()
    db.refresh(product_type)
    return product_type

# Retrieve a ProductType entry by ID
@app.get("/product_type/{product_type_id}/")
def read_product_type(product_type_id: int, db: Session = Depends(get_db)):
    product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    return product_type

# Retrieve all ProductType entries
@app.get("/product_type/")
def read_product_types(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    product_types = db.query(ProductType).offset(skip).limit(limit).all()
    return product_types

# Update a ProductType entry by ID
@app.put("/product_type/{product_type_id}/")
def update_product_type(product_type_id: int, product_type: ProductType, db: Session = Depends(get_db)):
    db_product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    
    db_product_type.product_type_desc = product_type.product_type_desc
    db_product_type.update_dt = product_type.update_dt
    db_product_type.updated_by = product_type.updated_by
    db.commit()
    db.refresh(db_product_type)
    return db_product_type

# Delete a ProductType entry by ID
@app.delete("/product_type/{product_type_id}/")
def delete_product_type(product_type_id: int, db: Session = Depends(get_db)):
    product_type = db.query(ProductType).filter(ProductType.id == product_type_id).first()
    if product_type is None:
        raise HTTPException(status_code=404, detail="ProductType not found")
    
    db.delete(product_type)
    db.commit()
    return product_type

# Create a Products entry
@app.post("/products/")
def create_products(products: Products, db: Session = Depends(get_db)):
    db.add(products)
    db.commit()
    db.refresh(products)
    return products

# Retrieve a Products entry by ID
@app.get("/products/{product_id}/")
def read_products(product_id: int, db: Session = Depends(get_db)):
    products = db.query(Products).filter(Products.id == product_id).first()
    if products is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return products

# Retrieve all Products entries
@app.get("/products/")
def read_all_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Products).offset(skip).limit(limit).all()
    return products

# Update a Products entry by ID
@app.put("/products/{product_id}/")
def update_products(product_id: int, products: Products, db: Session = Depends(get_db)):
    db_products = db.query(Products).filter(Products.id == product_id).first()
    if db_products is None:
        raise HTTPException(status_code=404, detail="Products not found")
    
    db_products.product_name = products.product_name
    db_products.product_type_id = products.product_type_id
    db_products.created_by = products.created_by
    db_products.created_dt = products.created_dt
    db_products.updated_by = products.updated_by
    db_products.updated_dt = products.updated_dt
    db_products.parent_product_id = products.parent_product_id
    db.commit()
    db.refresh(db_products)
    return db_products

# Delete a Products entry by ID
@app.delete("/products/{product_id}/")
def delete_products(product_id: int, db: Session = Depends(get_db)):
    products = db.query(Products).filter(Products.id == product_id).first()
    if products is None:
        raise HTTPException(status_code=404, detail="Products not found")
    
    db.delete(products)
    db.commit()
    return products

# Create a ProductPrice entry
@app.post("/product_price/")
def create_product_price(product_price: ProductPrice, db: Session = Depends(get_db)):
    db.add(product_price)
    db.commit()
    db.refresh(product_price)
    return product_price

# Retrieve a ProductPrice entry by ID
@app.get("/product_price/{product_price_id}/")
def read_product_price(product_price_id: int, db: Session = Depends(get_db)):
    product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    return product_price

# Retrieve all ProductPrice entries
@app.get("/product_price/")
def read_all_product_price(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    product_prices = db.query(ProductPrice).offset(skip).limit(limit).all()
    return product_prices

# Update a ProductPrice entry by ID
@app.put("/product_price/{product_price_id}/")
def update_product_price(product_price_id: int, product_price: ProductPrice, db: Session = Depends(get_db)):
    db_product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if db_product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    
    db_product_price.product_id = product_price.product_id
    db_product_price.usd_price = product_price.usd_price
    db_product_price.pricing_start_dt = product_price.pricing_start_dt
    db_product_price.pricing_end_dt = product_price.pricing_end_dt
    db_product_price.created_by = product_price.created_by
    db_product_price.created_dt = product_price.created_dt
    db_product_price.updated_by = product_price.updated_by
    db_product_price.updated_dt = product_price.updated_dt
    db.commit()
    db.refresh(db_product_price)
    return db_product_price

# Delete a ProductPrice entry by ID
@app.delete("/product_price/{product_price_id}/")
def delete_product_price(product_price_id: int, db: Session = Depends(get_db)):
    product_price = db.query(ProductPrice).filter(ProductPrice.id == product_price_id).first()
    if product_price is None:
        raise HTTPException(status_code=404, detail="ProductPrice not found")
    
    db.delete(product_price)
    db.commit()
    return product_price

# Create a ProductPriceHistory entry
@app.post("/product_price_history/")
def create_product_price_history(product_price_history: ProductPriceHistory, db: Session = Depends(get_db)):
    db.add(product_price_history)
    db.commit()
    db.refresh(product_price_history)
    return product_price_history

# Retrieve a ProductPriceHistory entry by ID
@app.get("/product_price_history/{product_price_history_id}/")
def read_product_price_history(product_price_history_id: int, db: Session = Depends(get_db)):
    product_price_history = db.query(ProductPriceHistory).filter(ProductPriceHistory.id == product_price_history_id).first()
    if product_price_history is None:
        raise HTTPException(status_code=404, detail="ProductPriceHistory not found")
    return product_price_history

# Retrieve all ProductPriceHistory entries
@app.get("/product_price_history/")
def read_all_product_price_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    product_price_histories = db.query(ProductPriceHistory).offset(skip).limit(limit).all()
    return product_price_histories

# Update a ProductPriceHistory entry by ID
@app.put("/product_price_history/{product_price_history_id}/")
def update_product_price_history(product_price_history_id: int, product_price_history: ProductPriceHistory, db: Session = Depends(get_db)):
    db_product_price_history = db.query(ProductPriceHistory).filter(ProductPriceHistory.id == product_price_history_id).first()
    if db_product_price_history is None:
        raise HTTPException(status_code=404, detail="ProductPriceHistory not found")
    
    db_product_price_history.product_id = product_price_history.product_id
    db_product_price_history.usd_price = product_price_history.usd_price
    db_product_price_history.pricing_start_dt = product_price_history.pricing_start_dt
    db_product_price_history.pricing_end_dt = product_price_history.pricing_end_dt
    db_product_price_history.created_by = product_price_history.created_by
    db_product_price_history.created_dt = product_price_history.created_dt
    db_product_price_history.updated_by = product_price_history.updated_by
    db_product_price_history.updated_dt = product_price_history.updated_dt
    db.commit()
    db.refresh(db_product_price_history)
    return db_product_price_history

# Delete a ProductPriceHistory entry by ID
@app.delete("/product_price_history/{product_price_history_id}/")
def delete_product_price_history(product_price_history_id: int, db: Session = Depends(get_db)):
    product_price_history = db.query(ProductPriceHistory).filter(ProductPriceHistory.id == product_price_history_id).first()
    if product_price_history is None:
        raise HTTPException(status_code=404, detail="ProductPriceHistory not found")
    
    db.delete(product_price_history)
    db.commit()
    return product_price_history