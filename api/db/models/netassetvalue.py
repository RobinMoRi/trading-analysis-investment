from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db.models.company import Company

from db.database import Base

class NetAssetValue(Base):
    __tablename__ = "net_asset_values"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ticker = Column(String, unique=True, index=True)
    price = Column(Float, unique=False, index=True)
    company_id = Column(Integer, ForeignKey(Company.id), nullable=False)
    