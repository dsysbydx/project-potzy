import sys
import pandas as pd
import numpy as np
import time
sys.path.append('../potzy/')

#LOG IN INTO SIAMCHART
import potzy.siamchartdatareader as scdr
dr=scdr.SiamChartDataReader()
dr.loginToSiamChart()

all_thai_tickers = potzy.metadata.getAllThaiTickers()

num_round=0
today = dt.date.today()
year,month,day=today.year, today.month, today.day
potzy.helpers.ensure_dir()

while len(tickers_left) > 0 and num_round < 10:
    for ticker in tickers_left:
        try:
            tryRelogin=False
            while True:
                print('Loading data for ',ticker)
                df_fs=dr.getFinancialData(ticker)
                df_div=dr.getDividendData(ticker)
                print('Done for ticker ',ticker,' size of dividend and fs df are ',len(df_div),len(df_fs))
                if len(df_fs) <= 5 and not tryRelogin:
                    try:
                        dr.loginToSiamChart()
                    except:
                        print('log in not successful, probably stil in login session')
                    tryRelogin=True
                    time.sleep(1)
                    print(ticker, ": relogin and reload the data ... ")
                else:
                    break

            #reorganize columns
            prefix_cols=['revenue','net_profit','eps','dps','gross_profit','ebit','ebitda']
            cols=prefix_cols+[x for x in df_fs.columns if x not in prefix_cols]
            df_fs=df_fs[cols]

            #save result
            filename='/'.join([str(year),str(month),str(day),ticker])
            df_fs.to_csv('../data/siamchart/fs/'+filename+'.csv')
            df_div.to_csv('../data/siamchart/div/'+filename+'.csv')

            #
            tickers_loaded.add(ticker)

        except:
            #raise
            print('Error loading information for ticker ',ticker)
            bad_tickers.add(ticker)

    tickers_left = tickers_left.difference(tickers_loaded)
    num_round+=1
