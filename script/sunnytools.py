import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
sns.set_style('darkgrid')
plt.rcParams['figure.figsize'] = (10.0, 5.0)
pd.set_option('display.max_rows', 500)

# import pandas_datareader as pdr #error from version

def ensure_dir(file_path):
    import os
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


# PANDAS HELPER FUNCTIONS
def getDictFromDataframe(df,keyCol,valueCol):
    return df.set_index(keyCol).to_dict()[valueCol]

def getRearrangeColumns(df,prefixCols):
    return prefixCols+[x for x in df.columns if x not in prefixCols]


# Valuation related functions
def forwardPE(eps_latest,growth,pe_terminal,payout_ratio,discount_rate):
    N=len(growth)
    eps=eps_latest
    value=0
    for i in range(N):
        g=growth[i]
        eps=eps*(1+g)
        dividend=eps*payout_ratio
        value+=dividend/((1+discount_rate)**(i+1))

    #get present value di
    value+=eps*pe_terminal/((1+discount_rate)**(N))
    return value


def dividend_discounted_model(eps_next, growth, growth_terminal, discount_rate, payout_ratio, payout_ratio_terminal, nextDate, numYear=10):
    # if numyear is too short, get
    numYear = max(numYear, len(growth) + 1)

    # add date
    dates = [dt.date(nextDate.year + i, nextDate.month, nextDate.day) for i in range(numYear)]
    df = pd.DataFrame(index=dates, columns=['eps', 'dps', 'value'])

    # for each date, get free cash flow
    eps = [0.0] * numYear
    eps[0] = eps_next
    for i in range(numYear - 1):
        g = growth[i] if i < len(growth) else growth_terminal
        eps[i + 1] = eps[i] * (1 + g)

    # get payout
    payout_ratio_list = [payout_ratio] * len(growth) + [payout_ratio_terminal] * (numYear - len(growth))

    # get eps
    dps = [eps[i] * payout_ratio_list[i] for i in range(numYear)]

    # for each date, get valuation
    value = [0.0] * numYear
    beta = (1 + growth_terminal) / (1 + discount_rate)
    value[-1] = dps[-1] / (1 - beta)
    for i in range(numYear - 1):
        value[-i - 2] = dps[-i - 2] + value[-i - 1] / (1 + discount_rate)

    # store in df
    df['eps'] = eps
    df['dps'] = dps
    df['value'] = value
    df['p/e'] = df['value'] / df['eps']

    return df


def discounted_cashflow_model(fcf_next, growth, growth_terminal, discount_rate, payout_ratio, nextDate, numYear=10):
    # if numyear is too short, get
    numYear = max(numYear, len(growth) + 1)

    # add date
    dates = [dt.date(nextDate.year + i, nextDate.month, nextDate.day) for i in range(numYear)]
    df = pd.DataFrame(index=dates, columns=['fcf', 'value'])

    # for each date, get free cash flow
    fcf = [0.0] * len(df)
    fcf[0] = fcf_next
    for i in range(len(dates) - 1):
        g = growth[i] if i < len(growth) else growth_terminal
        fcf[i + 1] = fcf[i] * (1 + g)

    # for each date, get valuation
    value = [0.0] * len(df)
    beta = (1 + growth_terminal) / (1 + discount_rate)
    value[-1] = fcf[-1] / (1 - beta)
    for i in range(len(dates) - 1):
        value[-i - 2] = fcf[-i - 2] + value[-i - 1] / (1 + discount_rate)

    # store in df
    df['fcf'] = fcf
    df['value'] = value
    df['p/fcf'] = df['value'] / df['fcf']

    return df


THAI_TICKER_FILE = '../data/thai_tickers.p'
def getAllThaiTickers():
    #load data
    return np.load(THAI_TICKER_FILE)
