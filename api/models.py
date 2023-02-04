from sqlalchemy import Column, Integer, String, Float

from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    yf_ticker = Column(String, unique=True, index=True)
    url = Column(String, unique=True, index=True)
    html_element = Column(String, unique=False, index=True)
    price = Column(Float, unique=False, index=True)

    reported_type = Column(String, unique=False, index=True)
    reported_val = Column(String, unique=False, index=True)
    reported_weight = Column(Float, unique=False, index=True)
    reported_position = Column(Float, unique=False, index=True)
    reported_buy = Column(Float, unique=False, index=True)

    computed_type = Column(String, unique=False, index=True)
    computed_val = Column(String, unique=False, index=True)
    computed_weight = Column(Float, unique=False, index=True)
    computed_position = Column(Float, unique=False, index=True)
    computed_buy = Column(Float, unique=False, index=True)
    