from pydantic import BaseModel
from db.models.netassetvalue import AssetType
from db.models.netassetvalue import ValueType


class AssetValueBase(BaseModel):
    ticker: str
    val: float
    value_type: ValueType
    asset_type: AssetType

class AssetValue(AssetValueBase):
    id: int

    class Config:
        orm_mode = True

class AssetValueCreate(AssetValueBase):
    pass