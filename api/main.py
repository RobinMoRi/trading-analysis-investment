from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas, ibindex
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add one company to db
@app.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = crud.get_company_by_yf_ticker(db, yf_ticker=company.yf_ticker)
    if db_company:
        raise HTTPException(status_code=400, detail="Ticker already exists")
    return crud.create_company(db=db, company=company)

# update company db
# TODO: monitor ibindex.se and update accordingly
@app.post("/companies/update", response_model=List[schemas.Company])
def update_companies(db: Session = Depends(get_db)):
    companies = ibindex.get_ib_companies()
    print(companies)
    db_companies = []
    for company_dict in companies:
        company = schemas.CompanyCreate.parse_obj(company_dict)
        db_company = crud.get_company_by_yf_ticker(db, yf_ticker=company.yf_ticker)
        if db_company:
            pass
        else:
            temp = crud.create_company(db=db, company=company)
            db_companies.append(temp)
    return db_companies

# Get all companies from db
@app.get("/companies/", response_model=List[schemas.Company])
def read_company(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

# Get live price for db companies
@app.get("/companies/prices")
def read_prices(db: Session = Depends(get_db)):
    companies = crud.get_companies(db)
    prices = ibindex.get_prices(companies)
    return prices