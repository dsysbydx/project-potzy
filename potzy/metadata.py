import pandas as pd
import requests
import re

SET100_SIAMCHART_URL = 'http://siamchart.com/stock/SET100'
SET50_SIAMCHART_URL = 'http://siamchart.com/stock/SET50'


def get_all_thai_tickers():
    df = pd.read_csv('../data/meta/thai_stocks.csv', index_col=[0])
    return sorted(df.index.unique())


def get_set50_tickers():
    return None


def get_set100_tickers():
    return None


def read_set_table_siamchart(url):
    """read set-table from siamchart url,
    only test for set50,set100 page in siamchart."""
    res = requests.get(url)
    regex = '<a href="/stock-chart/\w*/'

    all_tickers = []
    for m in re.finditer(regex, res.text):
        link = str(m.group(0))
        ticker = link.split('/')[-2]
        all_tickers.append(ticker)
    return all_tickers


def load_set50_tickers():
    return read_set_table_siamchart(SET50_SIAMCHART_URL)


def load_set100_tickers():
    return read_set_table_siamchart(SET100_SIAMCHART_URL)
