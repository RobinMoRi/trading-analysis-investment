from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from db.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ticker = Column(String, unique=True, index=True)
    price = Column(Float, unique=False, index=True)
    net_asset_values = relationship('NetAssetValue', backref='company', lazy=True)
    