import requests
import string
import pandas as pd

SET_META_URL_PREFIX = 'https://www.set.or.th/set/commonslookup.do?language=th&country=TH&prefix='
OUTPUT_FILE = '../data/meta/thai_stocks.csv'

prefix_list = ["NUMBER"]+list(string.ascii_uppercase[:27])
stock_table = pd.DataFrame()
for prefix in prefix_list:
    stock_table = stock_table.append(pd.read_html(SET_META_URL_PREFIX+prefix)[0],ignore_index=True)
    
stock_table.columns = ['ticker','name','market']
stock_table.set_index('ticker',inplace=True)

#print result
print('Print thai stock metadata headers ...')
print(stock_table.head())
print('Saving result to ',OUTPUT_FILE)

#Save result
stock_table.to_csv(OUTPUT_FILE)