import pandas as pd
import json
from yahoo_fin.stock_info import get_live_price
from selenium import webdriver
from requests.utils import quote
import time

import lxml.html as lh
import re

DATA_PATH = '../data/ib_stocks_stockholm.csv'

# Read companies from csv file
def read_companies():
    # Read df and set nan to empty string
    stocks_df = pd.read_csv(DATA_PATH)
    stocks_df.fillna('', inplace=True)

    # Comply with format of yahoo finance for swedish stocks
    stocks_df['Ticker YF'] = stocks_df['Ticker'].str.replace(' ', '-')
    stocks_df['Ticker YF'] = stocks_df['Ticker'].astype(str) + '.ST'
    stocks_list_yf = stocks_df['Ticker'].tolist()

    # Return companies list
    companies = []
    for index, row in stocks_df.iterrows():
        temp = {}
        temp["ticker"] = row['Ticker']
        temp["yf_ticker"] = row['Ticker YF'].replace(' ', '-')
        temp["url"] = row['URL_PATH']
        temp["html_element"] = row['ELEMENT_NAME']
        companies.append(temp)

    return companies

# Get live prices from yahoo finance api
def get_prices(companies):
    prices = []
    for company in companies:
        temp = {}
        temp['yf_ticker'] = company.yf_ticker
        temp['price'] =  get_live_price(company.yf_ticker)
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

def compute_positions(portfolio_size, asset_values, prices):
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