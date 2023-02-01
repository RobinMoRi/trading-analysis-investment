import pandas as pd
import json
from yahoo_fin.stock_info import get_live_price

DATA_PATH = '../data/ib_stocks_stockholm.csv'

def get_ib_companies():
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


def get_prices(companies):
    prices = {}
    for company in companies:
        prices[company.yf_ticker] = get_live_price(company.yf_ticker)
    return prices