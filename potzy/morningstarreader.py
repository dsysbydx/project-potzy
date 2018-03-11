import pandas as pd
import urllib
from io import StringIO,BytesIO

MORNINGSTAR_THAI_KEY_RATIO_URL='http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&region=tha&t=XBKK:'
MORNINGSTAR_US_KEY_RATIO_URL='http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&region=us&t='

def load_key_ratio(ticker,region):
    if region[:2]=='th':
        return load_key_ratio_thai(ticker)
    elif region[:2]=='us':
        return load_key_ratio_us(ticker)

def load_key_ratio_thai(ticker):
    url=MORNINGSTAR_THAI_KEY_RATIO_URL+ticker.upper()
    html_source = urllib.request.urlopen(url).read()
    html_decode=html_source.decode("utf-8")
    df=pd.read_csv(StringIO(html_decode),sep=',',skiprows=2)

    ## clean up
    df.set_index(df.columns[0],inplace=True)
    df.index.name='item'

    return df

def load_key_ratio_us(ticker):
    url=MORNINGSTAR_US_KEY_RATIO_URL+ticker.upper()
    html_source = urllib.request.urlopen(url).read()
    html_decode=html_source.decode("utf-8")
    df=pd.read_csv(StringIO(html_decode),sep=',',skiprows=2)

    ## clean up
    df.set_index(df.columns[0],inplace=True)
    df.index.name='item'

    return df