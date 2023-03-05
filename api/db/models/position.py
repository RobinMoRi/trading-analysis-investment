
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from db.models.company import Company
from sqlalchemy.sql import func
from db.models.netassetvalue import ValueType
from db.database import Base

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    val = Column(Float, unique=False, index=True)
    weight = Column(Float, unique=False, index=True)
    position = Column(Float, unique=False, index=True)
    buy = Column(Float, unique=False, index=True)
    value_type = Column(Enum(ValueType), unique=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="positions")
    netassetvalue = relationship("NetAssetValue", back_populates="position")