import logging
from typing import List
from db.models.netassetvalue import AssetType
from db.models.netassetvalue import ValueType
from sqlalchemy.orm import Session, joinedload

# import models.models as models
from schemas.price import Price
from schemas.company import Company
from schemas.assetvalue import AssetValueCreate
from db.models.company import Company as companyModel
from db.models.netassetvalue import NetAssetValue as navModel
from db.models.position import Position as positionModel


def get_company_by_ticker(db: Session, ticker: str):
    return db.query(companyModel).filter(companyModel.ticker == ticker).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(companyModel).offset(skip).limit(limit).all()

def create_company(db: Session, company: Company):
    db_company = companyModel(ticker=company.ticker, yf_ticker=company.yf_ticker, name=company.name, price=company.price)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_prices(db: Session, prices: List[Price]):
    for price in prices:
        db.query(companyModel).filter(companyModel.yf_ticker == price['yf_ticker']).update({'price': price['price'], 'price_updated_at': price['price_updated_at']})
    db.commit()

def create_company_assetvalue(db: Session, asset_value: AssetValueCreate, company_id: int):
    db_net_asset_value = navModel(**asset_value, company_id=company_id)
    db.add(db_net_asset_value)
    db.commit()
    db.refresh(db_net_asset_value)
    return db_net_asset_value

def update_company_assetvalue(db: Session, asset_value: AssetValueCreate, asset_value_id: int):
    db_net_asset_value = navModel(**asset_value)
    db.query(navModel).filter(navModel.id == asset_value_id).update({'val': db_net_asset_value.val, 'asset_type': db_net_asset_value.asset_type})
    db.commit()
    return db_net_asset_value

def get_asset_value_by_type(db: Session, value_type: ValueType, company_id: int):
    return db.query(navModel).filter(navModel.value_type == value_type, navModel.company_id == company_id).first()

def get_asset_values(db: Session, asset_type: AssetType, value_type: ValueType, skip: int = 0, limit: int = 100):
    queryset = db.query(navModel)

    if(asset_type != ''):
        queryset = queryset.filter(navModel.asset_type == asset_type)

    if(value_type != ''):
        queryset = queryset.filter(navModel.value_type == value_type)

    return queryset.offset(skip).limit(limit).all()

def update_company_position(db: Session, position):
    db_positions = positionModel(**position)
    db.add(db_positions)
    db.commit()
    db.refresh(db_positions)
    return db_positions

def delete_company_position(db: Session):
    deleted = db.query(positionModel).delete()
    db.commit()
    return deleted

def get_company_positions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(positionModel).offset(skip).limit(limit).all()


def get_company_positions_deep(db: Session, skip: int = 0, limit: int = 100):
    return db.query(positionModel).options(joinedload(positionModel.netassetvalue)).options(joinedload(positionModel.company)).offset(skip).limit(limit).all()