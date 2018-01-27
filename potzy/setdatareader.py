
import pandas as pd

SET_PRICE_URL='https://www.set.or.th/set/historicaltrading.do?'

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

    print(pg,len(df),len(df.drop_duplicates()))
    df.drop_duplicates(inplace=True)
    df.columns=[x.lower() for x in df.columns]
    return df