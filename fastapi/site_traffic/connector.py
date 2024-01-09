from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from flask_sqlalchemy import SQLAlchemy
from pybigquery.api import ApiClient

#import the db_base libraries for all connections we have
from libraries.db_base import db_base

#ToDo:Change project name and dataset name.
#Provide the path to a service account JSON file
engine = create_engine('bigquery://', credentials_path='/data/school/MIDS/sql_server_work/dbs/servers/bigquery/bigquery1/tokens/brave-sonar-367918-74b1d5b6db90.json')

db = SQLAlchemy()

customers_db = db_base("customers","mysql")
products_db = db_base("products","mssql")
finance_db = db_base("finance","postsql")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
