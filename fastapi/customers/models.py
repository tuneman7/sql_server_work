from sqlalchemy import CHAR, Column, DateTime, Integer, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CustomerInfo(Base):
    __tablename__ = 'customer_info'

    id = Column(Integer, primary_key=True)
    f_name = Column(CHAR(100))
    l_name = Column(CHAR(100))
    email_address = Column(CHAR(200))
    country = Column(CHAR(100))
    postalcode = Column(CHAR(100))
    city_name = Column(CHAR(100))
    province = Column(CHAR(100))
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


class CustomerProduct(Base):
    __tablename__ = 'customer_product'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    product_id = Column(Integer)
    product_type_desc = Column(CHAR(100))
    purchase_dt = Column(DateTime)
    expiration_dt = Column(DateTime)
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)


class CustomerProductHistory(Base):
    __tablename__ = 'customer_product_history'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    product_id = Column(Integer)
    product_type_desc = Column(CHAR(100))
    purchase_dt = Column(DateTime)
    expiration_dt = Column(DateTime)
    created_by = Column(CHAR(100))
    created_dt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_by = Column(CHAR(100))
    updated_dt = Column(DateTime)
