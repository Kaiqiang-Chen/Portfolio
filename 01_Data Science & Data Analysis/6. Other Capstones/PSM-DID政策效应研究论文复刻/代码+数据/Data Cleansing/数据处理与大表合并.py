import pandas as pd
import openpyxl
df1 = pd.read_excel(r'商业数据分析\论文复现_陈凯强（代码+数据）\Raw Data\其他指标.xlsx')
df2 = pd.read_excel(r'商业数据分析\论文复现_陈凯强（代码+数据）\Raw Data\2006-2019年中国各城市PM2.5平均浓度.xlsx')

# 增加能源消耗
df3 = pd.read_excel(r'商业数据分析\论文复现_陈凯强（代码+数据）\Data Cleansing\energy_combine.xlsx')
df4 = pd.read_excel(r'商业数据分析\论文复现_陈凯强（代码+数据）\Raw Data\1997-2022年市场化指数.xlsx')

df=pd.merge(df1,df2,on=['code','year'],how="left")
df=pd.merge(df,df3,on=['code','year'],how="left")
df=pd.merge(df,df4,on=['pcode','year'],how="left")

# 增加能源消耗强度字段
df['energdp']=df['so2']*10000/df['gdp']

# 增加碳排放co2字段
df5 = pd.read_excel('商业数据分析\论文复现_陈凯强（代码+数据）\Raw Data\The_Emission_Inventories_for_290_Chinese_Cities_from_1997_to_2019.xlsx')

years = [year for year in range(2006, 2020)]  # 假设数据直到2019年

df6 = pd.melt(df5, id_vars=['city', 'code'], value_vars=years, var_name='year', value_name='co2') #长表变宽表
df6['year'] = df6['year'].astype(int)  # 将字符串转换为整数
df6.sort_values(by=['code', 'year'], inplace=True)
df6=df6[['code', 'year', 'co2']]
df=pd.merge(df,df6,on=['code','year'],how="left")

# 增加碳强度字段
df['cogdp']=df['co2']/df['gdp']

# 增加专利数字段
df7 = pd.read_excel(r'商业数据分析\论文复现_陈凯强（代码+数据）\Raw Data\2006-2019年283个地级市专利授权.xlsx')
df8=df7.drop('city', axis=1)
df=pd.merge(df,df8,on=['code','year'],how="left")



# 增加碳交易相关字段 
df8 = pd.read_excel(r'商业数据分析\论文复现_陈凯强（代码+数据）\Raw Data\碳交易数据.xlsx')
df8=df8.drop('city', axis=1)
df=pd.merge(df,df8,on=['code','year'],how="left")

# 使用to_excel方法将DataFrame保存为Excel文件
df.to_excel(r'商业数据分析\论文复现_陈凯强（代码+数据）\Data Cleansing\1_数据大表.xlsx', index=False)