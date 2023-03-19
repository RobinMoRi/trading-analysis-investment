
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from db.models.company import Company
from sqlalchemy.sql import func

from db.database import Base

class AssetType(enum.Enum):
    rebate = 0
    premium = 1

class ValueType(enum.Enum):
    reported = 0
    computed = 1

class NetAssetValue(Base):
    __tablename__ = "net_asset_values"

    id = Column(Integer, primary_key=True, index=True)
    val = Column(Float, unique=False, index=True)
    ticker = Column(String, unique=False, index=True)
    asset_type = Column(Enum(AssetType), unique=False)
    value_type = Column(Enum(ValueType), unique=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="netassetvalues")
    position = relationship("Position", back_populates="netassetvalue")