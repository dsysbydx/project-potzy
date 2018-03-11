
import pandas as pd
import requests
import string
from urllib.parse import urlencode

SET_PRICE_URL='https://www.set.or.th/set/historicaltrading.do?'
SET_META_URL_MAIN = 'https://www.set.or.th/dat/eod/listedcompany/static/listedCompanies_en_US.xls'
OUTPUT_META_FILE = '../data/meta/thai_stocks.csv'

def load_price_data_from_set(ticker):
    df=pd.DataFrame()
    pg=0
    while True:
        url=SET_PRICE_URL+urlencode({'symbol':ticker,'page':pg, "language":'en','country':'US','type':'trading'})       
        df=df.append(pd.read_html(url)[0])
        if len(df)>len(df.drop_duplicates()):
            break
        else:
            pg+=1
    #print(pg,len(df),len(df.drop_duplicates()))
    df.drop_duplicates(inplace=True)
    df.columns=[x.lower() for x in df.columns]
    
    return df


def load_all_tickers(save_to_csv=False):

    stock_table = pd.read_html(SET_META_URL_MAIN)[0]

    #first row is empthy, second row is the column
    columns = stock_table.iloc[1]
    stock_table = stock_table.iloc[2:]

    #set column, index
    stock_table.columns = [x.lower() for x in columns]
    stock_table.set_index('symbol',inplace=True)
    stock_table.index.name='ticker'

    if save_to_csv:
        stock_table.to_csv(OUTPUT_META_FILE)

    return stock_table
    
