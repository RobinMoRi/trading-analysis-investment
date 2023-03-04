from typing import List, Union

from pydantic import BaseModel

class CompanyBase(BaseModel):
    ticker: str
    yf_ticker: str
    name: str
    price: float

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True

class CompanyCreate(CompanyBase):
    pass