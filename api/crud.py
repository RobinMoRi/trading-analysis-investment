from typing import List

from sqlalchemy.orm import Session

# import models.models as models
from schemas.price import Price
from schemas.company import Company
from schemas.assetvalue import AssetValueCreate
from db.models.company import Company as companyModel
from db.models.netassetvalue import NetAssetValue as navModel


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

# ## TOOD: Clean this solution up... must be a better way
# def get_asset_values(db: Session, skip: int = 0, limit: int = 100):
    # asset_values = db.query(models.Company.yf_ticker, \
    #                 models.Company.reported_val, models.Company.reported_type, \
    #                 models.Company.computed_val, models.Company.computed_type).offset(skip).limit(limit).all()
    # arr = []
    # for row in asset_values:
    #     temp = {}
    #     temp['yf_ticker'] = row[0]
    #     temp['reported_val'] = float(row[1])
    #     temp['reported_type'] = row[2]
    #     temp['computed_val'] = float(row[3])
    #     temp['computed_type'] = row[4]
    #     arr.append(temp)
    # return arr




# def update_asset_values(db: Session, asset_values):
#     for val in asset_values:
#         db.query(models.Company).filter(models.Company.yf_ticker == val['yf_ticker']). \
#             updaxte({'reported_val': val['reported_val'], 'reported_type': val['reported_type'], \
#                     'computed_val': val['computed_val'], 'computed_type': val['computed_type'] })
#     db.commit()

# def update_positions(db: Session, positions):
#     for val in positions:
#         db.query(models.Company).filter(models.Company.yf_ticker == val['yf_ticker']). \
#             update({'reported_weight': val['reported_weight'], 'computed_weight': val['computed_weight'], \
#                     'reported_position': val['reported_position'], 'computed_position': val['computed_position'], \
#                     'reported_buy': val['reported_buy'], 'computed_buy': val['computed_buy'] })
#     db.commit()