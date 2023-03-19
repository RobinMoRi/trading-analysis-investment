import pandas as pd
import json
from yahoo_fin.stock_info import get_live_price
from selenium import webdriver
from requests.utils import quote
import requests
import time
from datetime import datetime
from sqlalchemy.sql import func

import lxml.html as lh
import re

from db.models.company import Company as CompanyModel
from db.models.netassetvalue import NetAssetValue as NAVModel

DATA_PATH = '../data/ib_stocks_stockholm.csv'

def read_companies_ibindex_api():
    resp = requests.get("https://ibindex.se/ibi//index/getProducts.req")
    companies = []
    for el in resp.json():
        temp = {}
        temp["ticker"] = el['product']
        temp["yf_ticker"] = el['product'].replace(' ', '-') + '.ST'
        temp["name"] = el['productName']
        temp["price"] = 0.0 #init price (using yahoo finance to fetch price)
        companies.append(temp)
    return companies

def read_asset_values_ibindex_api():
    resp = requests.get("https://ibindex.se/ibi//index/getProducts.req")
    nva = []
    for el in resp.json():
        #Computed
        temp = {}
        temp["ticker"] = el['product']
        temp["val"] = abs(el['netAssetValueCalculatedRebatePremium'])
        temp["value_type"] = 'computed'
        temp["asset_type"] = 'rebate' if el['netAssetValueCalculatedRebatePremium'] > 0 else 'premium'
        nva.append(temp)

        #Reported
        temp = {}
        temp["ticker"] = el['product']
        temp["val"] = abs(el['netAssetValueRebatePremium'])
        temp["value_type"] = 'reported'
        temp["asset_type"] = 'rebate' if el['netAssetValueRebatePremium'] > 0 else 'premium'
        nva.append(temp)

    return nva

# Get live prices from yahoo finance api
def get_prices(companies):
    prices = []
    for company in companies:
        temp = {}
        temp['yf_ticker'] = company.yf_ticker
        try:
            temp['price'] =  get_live_price(company.yf_ticker)
            temp['price_updated_at'] = datetime.now()
        except:
            temp['price'] = None
            temp['price_updated_at'] = None
        prices.append(temp)
    return prices

def compute_positions(db, portfolio_size, asset_values, companies):
    computed_rebates_sum = db.query(func.sum(NAVModel.val).filter(
        NAVModel.value_type == 'computed', NAVModel.asset_type == 'rebate'
    ).label("val")).first()[0]

    reported_rebates_sum = db.query(func.sum(NAVModel.val).filter(
        NAVModel.value_type == 'reported', NAVModel.asset_type == 'rebate'
    ).label("val")).first()[0]


    computed_rebates = asset_values.filter(
        NAVModel.value_type == 'computed', NAVModel.asset_type == 'rebate'
    ).all()

    reported_rebates = asset_values.filter(
        NAVModel.value_type == 'reported', NAVModel.asset_type == 'rebate'
    ).all()

    #Compute weights
    reported = compute_positions_helper(portfolio_size, reported_rebates, companies, reported_rebates_sum, 'reported')
    computed = compute_positions_helper(portfolio_size, computed_rebates, companies, computed_rebates_sum, 'computed')

    return {'reported': reported, 'computed': computed}

# TODO: probably not how it should be done....
def compute_positions_helper(portfolio_size, rebates, companies, rebates_sum, value_type):
    rows = []
    weightSum = 0
    for rebate in rebates:
        weight = rebate.val/rebates_sum
        weightSum += weight
        position = weight*portfolio_size
        company_price = companies.filter(CompanyModel.id == rebate.company_id).all()[0].price
        try:
            buy = position/company_price
        except:
            buy = None
        row = {
            'weight': weight,
            'position': position,
            'buy': buy,
            'value_type': value_type,
            'company_id': rebate.company_id,
            'netassetvalue_id': rebate.id,
        }
        rows.append(row)
    #Double check that the weight sum becomes 100% (as it should)
    print('Weight sum: ', weightSum)
    return rows
