import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
sns.set_style('darkgrid')
plt.rcParams['figure.figsize'] = (10.0, 5.0)
pd.set_option('display.max_rows', 500)
import sys

##sys.path.append('/Users/Sunny/GoogleDrive/SunnyDoc/Investment/ProjectPotzy/python/')
#from LoadDataMorningStar import *
#import pandas_datareader as pdr #error from version


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return None

## PANDAS HELPER FUNCTIONS
def getDictFromDataframe(df,keyCol,valueCol):
    return df.set_index(keyCol).to_dict()[valueCol]

def getRearrangeColumns(df,prefixCols):
    return prefixCols+[x for x in df.columns if x not in prefixCols]


