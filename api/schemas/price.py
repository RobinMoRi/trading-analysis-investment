from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Price(BaseModel):
    yf_ticker: str
    price: Optional[float] = None
    price_updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True