import pandas as pd
import numpy as np

df = pd.read_csv('/Users/sunny/GoogleDrive/SunnyDoc/StockData/thai_stocks_price_data_siamchart_plus_set.csv',index_col=[0])
df.index = pd.DatetimeIndex(df.index).date
df.index.name='date'

#add previous date for debugging
#df.sort_index(inplace=True)
#df['close_prev']=df.groupby('ticker')['close'].transform(lambda x: x.shift(1))
#df['close_next']=df.groupby('ticker')['close'].transform(lambda x: x.shift(-1))

### load splitting data
df_split = pd.read_csv('../data/meta/thai_stock_splitting.csv',index_col=[0])
df_split['date']=pd.to_datetime(df_split['date'].astype('str'),format='%Y-%m-%d').dt.date
df_split.set_index('date',inplace=True)
df_split.sort_index(inplace=True)

## add cumulative adj_factor
df_split['adj_factor']=df_split['par']*1.0/df_split['par_prev']
df_split['cum_adj_factor']=df_split.groupby('ticker')['adj_factor'].transform(lambda x: np.cumprod(x[::-1])[::-1])

## merge 
print(len(df),len(df_split))
cols=['date','ticker','cum_adj_factor']
df=pd.merge(df.reset_index(),df_split.reset_index()[cols],how='outer',on=['date','ticker']).set_index('date')
print(len(df))

df.sort_index(inplace=True)
tmp=df.groupby('ticker')['cum_adj_factor'].transform(lambda x: x.fillna(method='bfill').fillna(1.0).shift(-1))
df['adj_factor']=tmp.values
del tmp

## adjust price
price_cols = ['open','high','low','close']
adj_price_cols = ['adj_'+x for x in price_cols]
for i in range(len(price_cols)):
    df[adj_price_cols[i]]=df[price_cols[i]]*df['adj_factor']
    
df=df[['ticker']+price_cols+adj_price_cols+['adj_factor']]

df.to_csv('../data/price/thai_price_all_20170304.csv')