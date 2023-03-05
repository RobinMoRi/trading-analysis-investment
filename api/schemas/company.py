from typing import List, Union
from typing import Optional
from pydantic import BaseModel

class CompanyBase(BaseModel):
    ticker: str
    yf_ticker: str
    name: str
    price: Optional[float] = None

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True

class CompanyCreate(CompanyBase):
    pass