from sqlalchemy import Column, Integer, String

from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    yf_ticker = Column(String, unique=True, index=True)
    url = Column(String, unique=True, index=True)
    html_element = Column(String, unique=False, index=True)