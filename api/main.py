from typing import List
import logging
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.base import Base
from fastapi.middleware.cors import CORSMiddleware

import ibindex, crud
from schemas.company import Company, CompanyCreate
from schemas.price import Price
from schemas.position import Position
from schemas.assetvalue import AssetValue
from db.models.netassetvalue import AssetType
from db.models.netassetvalue import ValueType
from db.models.company import Company as CompanyModel
from db.models.netassetvalue import NetAssetValue as NAVModel

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#TODO: add column to track if ibindex is using mentioned company or not...
@app.post("/companies/update", response_model=List[Company])
def update_companies(db: Session = Depends(get_db)):
    companies = ibindex.read_companies_ibindex_api()
    db_companies = []
    for company_dict in companies:
        company = CompanyCreate.parse_obj(company_dict)
        db_company = crud.get_company_by_ticker(db, ticker=company.ticker)
        if db_company:
            pass
        else:
            temp = crud.create_company(db=db, company=company)
            db_companies.append(temp)
    return db_companies

# Get all companies from db
@app.get("/companies/", response_model=List[Company])
def read_company(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

# Update prices for companies
@app.post("/companies/prices", response_model=List[Price])
def update_prices(db: Session = Depends(get_db)):
    companies = crud.get_companies(db)
    prices = ibindex.get_prices(companies)
    crud.update_prices(db, prices)
    return prices

# Read db prices (not live data - only since last update)
@app.get("/companies/prices", response_model=List[Price])
def get_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prices = crud.get_companies(db, skip=skip, limit=limit)
    return prices

# Fill db with asset values
@app.post("/companies/asset-values", response_model=List[AssetValue])
def update_asset_values(db: Session = Depends(get_db)):
    net_asset_values = ibindex.read_asset_values_ibindex_api()
    result = []
    for nva in net_asset_values:
        db_company = crud.get_company_by_ticker(db, ticker=nva['ticker'])
        db_asset_value = crud.get_asset_value_by_type(db, nva['value_type'], db_company.id)
        if db_asset_value:
            crud.update_company_assetvalue(db, nva, db_asset_value.id)
            db_asset_value = crud.get_asset_value_by_type(db, nva['value_type'], db_company.id) #Get updated row
            asset_value = db_asset_value
        else:
            asset_value = crud.create_company_assetvalue(db, nva, db_company.id)
        result.append(asset_value)
    return result

# Read db prices (not live data - only since last update)
@app.get("/companies/asset-values", response_model=List[AssetValue])
def get_asset_values(asset_type: str = '', value_type: str = '', skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    asset_values = crud.get_asset_values(db, asset_type=asset_type, value_type=value_type, skip=skip, limit=limit)
    return asset_values

# Read positions (not live data - only since last update)
@app.get("/companies/positions", response_model=List[Position])
def get_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    positions = crud.get_company_positions(db, skip=skip, limit=limit)
    return positions

@app.post("/companies/positions", response_model=List[Position])
def update_positions(portfolio_size: int, db: Session = Depends(get_db)):
    asset_values_queryset = db.query(NAVModel)
    company_queryset = db.query(CompanyModel)

    calculations = ibindex.compute_positions(db, portfolio_size, asset_values_queryset, company_queryset)

    deleted = crud.delete_company_position(db)
    print(deleted)
    result = []
    for reported in calculations['reported']:
        temp = crud.update_company_position(db, reported)
        result.append(temp)
    
    for reported in calculations['computed']:
        temp = crud.update_company_position(db, reported)
        result.append(temp)
    return result