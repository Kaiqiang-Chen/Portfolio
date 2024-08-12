import tushare as ts

pro = ts.pro_api('ca0cd5409f62a54869ffa4ad1f81f99e0a3d649f4e87cfc034dc0010')
ts_code = '600519.SH'


# 获取股价等行情数据
def fetch_stock_price():
    df = pro.daily(ts_code=ts_code, period='20200101')
    print("获取股价等行情数据")
    print(df)
    return df


# 获取利润表数据
def fetch_profit():
    df = pro.income(ts_code=ts_code)
    # 获取利润表指定科目数据
    # df = pro.income(ts_code='600519.SH', period='20201231',
    #                 fields='ts_code,end_date,total_revenue,total_cogs,n_income,ebit')
    print("获取利润表数据")
    print(df)
    return df


if __name__ == '__main__':
    fetch_stock_price()
    fetch_profit()

