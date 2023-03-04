from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.base import Base

import ibindex, crud
from schemas.company import Company, CompanyCreate
from schemas.price import Price
from schemas.assetvalue import AssetValue
# import models.models as models
# import schemas.company as companySchema
# import schemas.price as priceSchema
# import schemas.assetvalue as assetvalueSchema
# import schemas.position as positionSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()

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
        asset_value = crud.create_company_assetvalue(db, nva, db_company.id)
        result.append(asset_value)
    return result

# # Read db prices (not live data - only since last update)
# @app.get("/companies/asset-values", response_model=List[assetvalueSchema.AssetValue])
# def get_asset_values(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     asset_values = crud.get_asset_values(db, skip=skip, limit=limit)
#     return asset_values


# @app.post("/companies/positions", response_model=List[positionSchema.Position])
# def update_positions(portfolio_size: int, db: Session = Depends(get_db)):
#     asset_values = crud.get_asset_values(db)
#     prices = crud.get_company_prices(db)
#     positions = ibindex.compute_positions(portfolio_size, asset_values, prices)
#     crud.update_positions(db, positions)
#     return positions

# # Read positions (not live data - only since last update)
# @app.get("/companies/positions", response_model=List[positionSchema.Position])
# def get_positions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     positions = crud.get_companies(db, skip=skip, limit=limit)
#     return positions

# # # Compute positions
# ## Compute weights
# ## Compute positions
# ## Compute number of shares to buy

# # @app.post("/companies/positions", response_model=List[assetvalueSchema.AssetValue])
# # def compute_positions(db: Session = Depends(get_db)):
# #     companies = crud.get_companies(db)
# #     asset_values = ibindex.get_asset_values(companies)
# #     crud.update_asset_values(db, asset_values)
# #     return asset_values