from pydantic import BaseModel

class AssetValue(BaseModel):
    yf_ticker: str
    reported_val: float
    reported_type: str
    computed_val: float
    computed_type: str

    class Config:
        orm_mode = True