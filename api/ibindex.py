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

# Get asset value dictionary for all companies in db
def get_asset_values(companies):
    html_pages = crawl_pages('https://ibindex.se/ibi/#/', companies)
    asset_values = create_asset_values(html_pages, companies)
    return asset_values


## ---------- Utility functions -------------
# Crawl pages on ibindex website to look for asset value (premium/rebate)
def crawl_pages(base_url, companies):
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(10)

    html_pages = {}
    for company in companies:
        url_ending = company.url
        driver.get(f'{base_url}{quote(url_ending)}')
        driver.refresh()
        time.sleep(4)
        html = driver.page_source
        html_pages[company.ticker] = html
    driver.quit()
    return html_pages

# Clean html docs into a more readable format for the various companies
def create_asset_values(html_pages, companies):
    asset_values = []
    regexp_number = '(\d{1,2}.\d{1,2})'
    regexp_rebate_premium = '(rabatt|premie)'

    for company in companies:
        temp = {'yf_ticker': company.yf_ticker}
        doc = lh.fromstring(html_pages[company.ticker])
        if(company.html_element != ''):
            rebate_premium_list = doc.xpath(f'//{company.html_element}//span')
        else:
            rebate_premium_list = doc.xpath('//app-company-current-rebate-premium//span')
        vals = [el.text for el in rebate_premium_list]
        if(len(vals) == 6):
            temp['computed_val'] = float(re.search(regexp_number, vals[1]).group(1))
            temp['reported_val'] = float(re.search(regexp_number, vals[4]).group(1))
            temp['computed_type'] = re.search(regexp_rebate_premium, vals[2]).group(1)
            temp['reported_type'] = re.search(regexp_rebate_premium, vals[5]).group(1)
        else:
            temp['computed_val']  = 0
            temp['reported_val']  = 0
            temp['computed_type'] = 'premie'
            temp['reported_type'] = 'premie'

        asset_values.append(temp)
    return asset_values

# TODO: clean this one up a bit..
def compute_positions_deprecated(portfolio_size, asset_values, prices):
    prices_dict = convert_prices(prices)
    positions = []
    sums = get_asset_value_sum(asset_values)
    for row in asset_values:
        temp = {'yf_ticker': row['yf_ticker'], 'reported_weight': 0, 'computed_weight': 0, \
                'reported_position': 0, 'computed_position': 0, \
                'reported_buy': 0, 'computed_buy': 0}
        
        # Compute weights for rabatt type ib's
        if(row['reported_type'] == 'rabatt'):
            temp['reported_weight'] = row['reported_val']/sums['reported_sum']
        if(row['computed_type'] == 'rabatt'):
            temp['computed_weight'] = row['computed_val']/sums['computed_sum']

        # compute positions based on weights above
        temp['reported_position'] = temp['reported_weight']*portfolio_size
        temp['computed_position'] = temp['computed_weight']*portfolio_size

        # compute number of shares to buy
        temp['reported_buy'] = temp['reported_position']/prices_dict[row['yf_ticker']]
        temp['computed_buy'] = temp['computed_position']/prices_dict[row['yf_ticker']]

        positions.append(temp)
    return positions

def compute_positions(db, portfolio_size, asset_values, companies):
    # prices_dict = convert_prices(prices)
    
    computed_rebates_sum = db.query(func.sum(NAVModel.val).filter(
        NAVModel.value_type == 'computed', NAVModel.asset_type == 'rebate'
    ).label("val")).first()[0]

    reported_rebates_sum = db.query(func.sum(NAVModel.val).filter(
        NAVModel.value_type == 'reported', NAVModel.asset_type == 'rebate'
    ).label("val")).first()[0]

    # computed_rebates_sum = asset_values.filter(
    #     NAVModel.value_type == 'reported', NAVModel.asset_type == 'rebate'
    # )


    print(reported_rebates_sum, computed_rebates_sum)


    # positions = []
    # sums = get_asset_value_sum(asset_values)
    # for row in asset_values:
    #     temp = {'yf_ticker': row['yf_ticker'], 'reported_weight': 0, 'computed_weight': 0, \
    #             'reported_position': 0, 'computed_position': 0, \
    #             'reported_buy': 0, 'computed_buy': 0}
        
    #     # Compute weights for rabatt type ib's
    #     if(row['reported_type'] == 'rabatt'):
    #         temp['reported_weight'] = row['reported_val']/sums['reported_sum']
    #     if(row['computed_type'] == 'rabatt'):
    #         temp['computed_weight'] = row['computed_val']/sums['computed_sum']

    #     # compute positions based on weights above
    #     temp['reported_position'] = temp['reported_weight']*portfolio_size
    #     temp['computed_position'] = temp['computed_weight']*portfolio_size

    #     # compute number of shares to buy
    #     temp['reported_buy'] = temp['reported_position']/prices_dict[row['yf_ticker']]
    #     temp['computed_buy'] = temp['computed_position']/prices_dict[row['yf_ticker']]

    #     positions.append(temp)
    return []

def get_asset_value_sum(asset_values):
    reported_sum = 0
    computed_sum = 0
    for row in asset_values:
        if(row['reported_type'] == 'rabatt'):
            reported_sum += row['reported_val']
        if(row['computed_type'] == 'rabatt'):
            computed_sum += row['computed_val']
    return {'reported_sum': reported_sum, 'computed_sum': computed_sum}

def convert_prices(prices):
    result = {}
    for price in prices:
        result[price[0]] = float(price[1])
    return result