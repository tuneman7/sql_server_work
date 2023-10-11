from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Identity, Integer, String, text
from sqlalchemy.dialects.mssql import MONEY
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class ProductType(Base):
    __tablename__ = 'product_type'

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    product_type_desc = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'))
    create_dt = Column(DateTime, server_default=text('(getdate())'))
    created_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text('(suser_sname())'))
    update_dt = Column(DateTime)
    updated_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'))


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    product_name = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    product_type_id = Column(Integer)
    created_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text('(suser_sname())'))
    created_dt = Column(DateTime, server_default=text('(getdate())'))
    updated_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'))
    updated_dt = Column(DateTime)
    parent_product_id = Column(Integer)

    product_price = relationship('ProductPrice', back_populates='product')
    product_price_history = relationship('ProductPriceHistory', back_populates='product')


class ProductPrice(Base):
    __tablename__ = 'product_price'

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    usd_price = Column(MONEY, nullable=False)
    pricing_start_dt = Column(DateTime, nullable=False)
    pricing_end_dt = Column(DateTime, nullable=False)
    created_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text('(suser_sname())'))
    created_dt = Column(DateTime, server_default=text('(getdate())'))
    updated_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'))
    updated_dt = Column(DateTime)

    product = relationship('Products', back_populates='product_price')


class ProductPriceHistory(Base):
    __tablename__ = 'product_price_history'

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    usd_price = Column(MONEY, nullable=False)
    pricing_start_dt = Column(DateTime, nullable=False)
    pricing_end_dt = Column(DateTime, nullable=False)
    created_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text('(suser_sname())'))
    created_dt = Column(DateTime, server_default=text('(getdate())'))
    updated_by = Column(CHAR(100, 'SQL_Latin1_General_CP1_CI_AS'))
    updated_dt = Column(DateTime)

    product = relationship('Products', back_populates='product_price_history')
