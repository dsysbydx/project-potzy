
import pandas as pd
import urllib
from io import StringIO,BytesIO


### TO DO: ADD market 
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

def str_to_float(df):
    return df.str.replace(",", "").astype('float')


class KeyRatioData():

    EPS_ROW_TH = 'Earnings Per Share THB'
    EPS_ROW_US = 'Earnings Per Share USD'

    CF_ROW_TH = 'Operating Cash Flow THB Mil'
    CF_ROW_US = 'Operating Cash Flow USD Mil'

    NUMSHARES_ROW = 'Shares Mil'

    def __init__(self):
        self.data = {}
        
    def load_data(self,ticker,region):
        if (ticker,region) not in self.data.keys():
            self.data[(ticker,region)]=load_key_ratio(ticker,region) 
        
    def get_data(self,ticker,region):
        return self.data[(ticker,region)]

    def get_eps(self,ticker,region):
        return str_to_float(self.data[(ticker,region)].loc[self._get_eps_row(region)])

    def get_cf(self,ticker,region):
        return str_to_float(self.data[(ticker,region)].loc[self._get_cf_row(region)])
    
    def get_numshares(self,ticker,region):
        return str_to_float(self.data[(ticker,region)].loc[self._get_numshares_row(region)])

    def get_cfps(self,ticker,region):
        """get cashflow per share"""
        df = self.data[(ticker,region)]
        return str_to_float(df.loc[self._get_cf_row(region)])/str_to_float(df.loc[self._get_numshares_row(region)])
    
    def _get_eps_row(self,region):
        if region=='th':
            return self.EPS_ROW_TH
        elif region=='us':
            return self.EPS_ROW_US
        else:
            raise
    
    def _get_cf_row(self,region):
        if region=='th':
            return self.CF_ROW_TH
        elif region=='us':
            return self.CF_ROW_US
        else:
            raise

    def _get_numshares_row(self,region):
        return self.NUMSHARES_ROW


        