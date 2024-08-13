import pandas as pd
import openpyxl
total = pd.read_excel('商业数据分析\论文复现_陈凯强（代码+数据）\\2006-2019市级能源消费.xlsx')
prop = pd.read_excel('商业数据分析\论文复现_陈凯强（代码+数据）\地级市能源消费结构（煤炭占比）.xlsx')
df=pd.merge(total,prop,on=['city','year'],how="left")
columns_to_export = ['year','city','energy','strcoal']

# 使用to_excel方法将DataFrame保存为Excel文件
df.loc[:, columns_to_export].to_excel('商业数据分析\论文复现_陈凯强（代码+数据）\energy_combine.xlsx', index=False)