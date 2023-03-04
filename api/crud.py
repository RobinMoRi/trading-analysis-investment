from typing import List

from sqlalchemy.orm import Session

import models.models as models
import schemas.company as companySchema
import schemas.price as priceSchema


def get_company_by_yf_ticker(db: Session, yf_ticker: str):
    return db.query(models.Company).filter(models.Company.yf_ticker == yf_ticker).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def get_company_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company.yf_ticker, models.Company.price).offset(skip).limit(limit).all()

## TOOD: Clean this solution up... must be a better way
def get_asset_values(db: Session, skip: int = 0, limit: int = 100):
    asset_values = db.query(models.Company.yf_ticker, \
                    models.Company.reported_val, models.Company.reported_type, \
                    models.Company.computed_val, models.Company.computed_type).offset(skip).limit(limit).all()
    arr = []
    for row in asset_values:
        temp = {}
        temp['yf_ticker'] = row[0]
        temp['reported_val'] = float(row[1])
        temp['reported_type'] = row[2]
        temp['computed_val'] = float(row[3])
        temp['computed_type'] = row[4]
        arr.append(temp)
    return arr

def create_company(db: Session, company: companySchema.Company):
    db_company = models.Company(ticker=company.ticker, yf_ticker=company.yf_ticker, url=company.url, html_element=company.html_element, price=0.0, \
                                reported_type='', reported_val=0.0, reported_weight=0.0, reported_position=0.0, reported_buy=0.0, \
                                computed_type='', computed_val=0.0, computed_weight=0.0, computed_position=0.0, computed_buy=0.0)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_prices(db: Session, prices: List[priceSchema.Price]):
    for price in prices:
        db.query(models.Company).filter(models.Company.yf_ticker == price['yf_ticker']). \
            update({'price': price['price']})
    db.commit()

def update_asset_values(db: Session, asset_values):
    for val in asset_values:
        db.query(models.Company).filter(models.Company.yf_ticker == val['yf_ticker']). \
            update({'reported_val': val['reported_val'], 'reported_type': val['reported_type'], \
                    'computed_val': val['computed_val'], 'computed_type': val['computed_type'] })
    db.commit()

def update_positions(db: Session, positions):
    for val in positions:
        db.query(models.Company).filter(models.Company.yf_ticker == val['yf_ticker']). \
            update({'reported_weight': val['reported_weight'], 'computed_weight': val['computed_weight'], \
                    'reported_position': val['reported_position'], 'computed_position': val['computed_position'], \
                    'reported_buy': val['reported_buy'], 'computed_buy': val['computed_buy'] })
    db.commit()