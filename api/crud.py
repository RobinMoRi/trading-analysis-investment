from typing import List

from sqlalchemy.orm import Session

import models, schemas


def get_company_by_yf_ticker(db: Session, yf_ticker: str):
    return db.query(models.Company).filter(models.Company.yf_ticker == yf_ticker).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()


def create_company(db: Session, company: schemas.Company):
    db_company = models.Company(ticker=company.ticker, yf_ticker=company.yf_ticker, url=company.url, html_element=company.html_element)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item