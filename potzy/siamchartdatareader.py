from selenium import webdriver
import pandas as pd
import numpy as np

CHROME_DRIVER_LOC='/usr/local/bin/chromedriver'
SIAMCHART_URL='http://siamchart.com/stock-info/'
SIAMCHART_LOGIN_URL='http://siamchart.com/forum/showthread.php?152'
SIAMCHART_DIVIDEND_TABLE=1
SIAMCHART_FINANCIAL_TABLE=3

class SiamChartDataReader:
    """ data reader for the siam chart site.

    [TO BE FILLED]

    """
    
    def __init__(self,browser=None):

        if browser is None:
            self.browser=webdriver.Chrome(executable_path =CHROME_DRIVER_LOC)
        else:
            self.browser=browser

    def getThaiStockMetaData(self):
        return None

    def loginToSiamChart(self,username="vodkaman",password="Prospect4K"):
        self.browser.get(SIAMCHART_LOGIN_URL)
        script='document.getElementById("navbar_username").value=' +'"'+username+'"'
        self.browser.execute_script(script)
        script='document.getElementById("navbar_password").value=' +'"'+password+'"'
        self.browser.execute_script(script)
        self.browser.find_element_by_class_name('loginbutton').click()
        return None

    def urlencodeSiamChart(self,url):
        return url.replace('&','_26')

    def getUrl(self,ticker):
        url=SIAMCHART_URL+ticker.upper()+'/'
        url=self.urlencodeSiamChart(url)
        return url

    def getPageSource(self,ticker):
        self.browser.get(self.getUrl(ticker))
        self.browser.find_element_by_xpath("//div[@onclick='displayQoQ();']").click()
        return self.browser.page_source

    def getFinancialData(self,ticker,clean=True,adjust_quarterly=True):
        dfQ=pd.read_html(self.getPageSource(ticker))
        df=dfQ[SIAMCHART_FINANCIAL_TABLE].T
        if not clean:
            return df
        else:
            df=self.cleanFinancialData(df)
        if not adjust_quarterly:
            return df
        else:
            df=self.adjustQuarterlyResult(df,ticker)

        return df

    def getDividendData(self,ticker):
        """dfQ=format from reading pagesource from siamchart directly"""

        region='th'

        #load and store dividend
        dfQ=pd.read_html(self.getPageSource(ticker))
        dfDiv=dfQ[SIAMCHART_DIVIDEND_TABLE]
        dfDiv=dfDiv[2:]
        dfDiv.columns=['date','dividend','close_price','dividend_yield']
        dfDiv.set_index('date',inplace=True)
        dfDiv.index=pd.DatetimeIndex(dfDiv.index)
        dfDiv.index=dfDiv.index.date
        dfDiv.sort_index(inplace=True)

        return dfDiv


    # STATIC FUNCTIONS
    # the functions below are mainly used to clearn/adjust with the pandas dataframe
    # derived from running pd.read_html(..) on page source of siam chart
    @staticmethod
    def cleanFinancialData(df):

        region='th'

        #load and store financial data
        df=df.apply(lambda x: x.map(lambda x: str(x).split('(')[0]))
        df.set_index(0,inplace=True)
        df.rename(columns=df.iloc[0],inplace=True)
        df.drop(df.index[0],inplace=True)
        df.index.name=None
        def floatWithError(x):
            try:
                return float(x)
            except:
                return np.nan
        df=df.applymap(lambda x: floatWithError(x.replace(',','')))
        df=df.dropna(axis=1,thresh=0.1*len(df))
        df.index=pd.DatetimeIndex(df.index)
        df['month']=df.index.month
        df['year']=df.index.year
        df.index=df.index.date
        df.sort_index(inplace=True)

        #change column name
        columnChangeMap={'ราคาปิด':'close_price',
                         'รวมรายได้':'revenue',
                         'รวมค่าใช้จ่าย':'expense',
                         'กำไรขั้นต้น':'gross_profit',
                         'กำไรจากการดำเนินงาน':'operating_profit',
                         'EBIT':'ebit',
                         'EBITDA': 'ebitda',
                         'กำไรสุทธิ':'net_profit',
                         'เงินสด':'cash',
                        'ลูกหนี้และตั๋วเงินรับ':'account_receivable',
                         'สินค้าคงเหลือ':'inventory',
                         'สินทรัพย์หมุนเวียน':'current_asset',
                       'ที่ดินอาคารและอุปกรณ์':'property_plant_equipment',
                         'รวมสินทรัพย์':'total_asset',
                         'เบิกเกินบัญชีและเงินกู้ยืม':'short_term_loan',
                       'เจ้าหนี้และตั๋วเงินจ่าย':'account_payable',
                         'หนี้สินระยะยาวครบในหนึ่งปี':'current_portion_long_term_debt',
                       'หนี้สินหมุนเวียน':'current_liability',
                         'หนี้สินไม่หมุนเวียน':'non_current_liability',
                         'รวมหนี้สิน':'total_liability',
                       'มูลค่าหุ้นที่เรียกชำระแล้ว':'paid_in_capital',
                         'รวมส่วนของผู้ถือหุ้น':'total_equity',
                       'เงินสดจากการดำเนินงาน':'cash_flow_operation',
                         'เงินสดจากการลงทุน':'cash_flow_investment',
                         'เงินสดจากการจัดหาเงิน':'cash_flow_financing',
                       'ค่าเสื่อมราคาค่าตัดจำหน่าย':'depreciation',
                        'หนี้สูญและหนี้สงสัยจะสูญ':'allowance_doubtful_accounts'}
        df.rename(columns=columnChangeMap,inplace=True)

        return df

    @staticmethod
    def adjustQuarterlyResult(df,ticker):

        RETURN_COLUMN='net_profit'
        cols_subtract=['revenue', 'expense', 'gross_profit', 'operating_profit',
               'ebit', 'ebitda', 'net_profit', 'cash_flow_operation',
               'cash_flow_investment', 'cash_flow_financing', 'depreciation',
                'dividend']
        cols_divide=['P/E']
        cols_multiply=['ROA%', 'ROAA%', 'ROE%', 'ROAE%', 'ROCE%']

        df.sort_index(inplace=True)
        df['number_of_shares']=df[RETURN_COLUMN]/df['EPS']
        if 'DPS' in df.columns:
            df['dividend']=df['DPS']*df['number_of_shares']
        else:
            df['dividend']=0
        df['return_old']=df[RETURN_COLUMN]

        #ad-hoc adjustment for some ticker due to weird time-sync from siamchart
        first_quarter_month=3
        if ticker in ['AOT']:
            first_quarter_month = 12

        for col in cols_subtract:
            if col in df.columns:
                df['tmp'] = df[col].diff()
                df.ix[df.month != first_quarter_month,col] = df.ix[df.month != first_quarter_month,'tmp']
            else:
                print('Warning: essential column ',col,' is missing. Assigning NaN.')
                df[col]=np.nan
        df['eps'] = df['net_profit']/df['number_of_shares']
        df['dps'] = df['dividend']/df['number_of_shares']
        del df['tmp']

        #correct pe ratio and related columns
        for col in cols_divide:
            if col in df.columns:
                df[col]=df[col]*df['return_old']/df[RETURN_COLUMN]/4
            else:
                df[col]=np.nan

        #correct roe,roa and related stuff
        for col in cols_multiply:
            if col in df.columns:
                df[col]=df[col]/df['return_old']*df[RETURN_COLUMN]*4
            else:
                df[col]=np.nan

        return df




################################################################
################################################################
##  END OF CLASS DEFINTION
################################################################
################################################################
