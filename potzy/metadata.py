import pandas as pd

def get_all_thai_tickers():
	df = pd.read_csv('../data/meta/thai_stocks.csv',index_col=[0])
	return sorted(df.index.unique())