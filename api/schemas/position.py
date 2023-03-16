from pydantic import BaseModel

class Position(BaseModel):
    yf_ticker: str
    reported_weight: float
    computed_weight: float
    reported_position: float
    computed_position: float
    reported_buy: float
    computed_buy: float

    class Config:
        orm_mode = True

class PositionCreate(Position):
    pass