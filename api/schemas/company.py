from typing import List, Union

from pydantic import BaseModel

class CompanyBase(BaseModel):
    ticker: str
    yf_ticker: str
    url: str
    html_element: str
    

class Company(CompanyBase):
    id: int

    reported_type: str
    reported_val: float
    reported_weight: float
    reported_position: float
    reported_buy: float

    computed_type: str
    computed_val: float
    computed_weight: float
    computed_position: float
    computed_buy: float

    class Config:
        orm_mode = True

class CompanyCreate(CompanyBase):
    pass