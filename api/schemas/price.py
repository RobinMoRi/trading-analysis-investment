from pydantic import BaseModel

class Price(BaseModel):
    yf_ticker: str
    price: float

    class Config:
        orm_mode = True