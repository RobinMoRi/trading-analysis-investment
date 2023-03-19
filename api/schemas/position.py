from pydantic import BaseModel
from typing import Optional
from db.models.netassetvalue import ValueType
from schemas.company import Company

class Position(BaseModel):
    id: int
    val: Optional[float] = None
    weight: float
    position: float
    buy: Optional[float] = None
    value_type: ValueType
    company_id: int
    netassetvalue_id: int

    class Config:
        orm_mode = True

class PositionCreate(Position):
    pass