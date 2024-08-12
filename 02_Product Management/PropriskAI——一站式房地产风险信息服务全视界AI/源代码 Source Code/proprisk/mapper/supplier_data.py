import os, sys
from random import random, randint
from flask_cors import CORS
from flask import Flask, request, jsonify
from pymongo import MongoClient

# from util.chatUtil import generate_affected_reason
from proprisk.util.chatUtil import generate_affected_reason

client = MongoClient('mongodb://localhost:27017/')
db = client['gongyingshang']


# 查询供应商的基本信息
def search_base_supplier(supplier):
    collection = db['supplier_information']
    documents = collection.find({})
    for document in documents:
        # print(document['供应商'])
        if supplier == document['供应商']:
            return document
        elif '组织机构代码' in document and supplier == document['组织机构代码']:
            return document
    return None


# 通过房地产商名称以及供应商名称 查询供应商的基本信息
def search_base_supplier_by_name(real_estate, supplier):
    collection = db['supplier_information']
    documents = collection.find({})
    for document in documents:
        if real_estate == document['企业名称'] and supplier == document['供应商']:
            return document
    return None


# 查找供应商对应的房地产公司列表
def search_real_estate_list_by_supplier(supplier):
    collection = db['company_suppliers']
    collection_info = db['company_information']
    cursor = collection.find({})
    real_estate_list = []
    for document in cursor:
        if supplier == document['供应商']:
            real_estate_list.append(document)
    real_estate_companies = collection.distinct('企业名称', {'供应商': supplier})
    real_estate_info_list = collection_info.find({'企业名称': {'$in': real_estate_companies}})
    # print(real_estate_companies)
    # print(real_estate_info_list)
    # 将供应商信息与房地产公司信息连接起来
    result = []
    for info in real_estate_info_list:
        supplier_info = collection.find_one({'企业名称': info['企业名称'], '供应商': supplier})
        company_info = {
            '企业名称': info['企业名称'],
            '股票代码': info['股票代码'],  # 可以根据需要添加其他信息
            # 添加其他您需要的信息
            '供应商': supplier_info['供应商'],
            '采购金额(万元)': supplier_info['采购金额(万元)'],
            '报告期/公开时间': supplier_info['报告期/公开时间'],
            '数据来源': supplier_info['数据来源']
        }
        result.append(company_info)
    return result


# 查找会对供应商造成影响的房地产公司列表
def search_real_estate_affected_list_by_supplier(supplier):
    collection_affected = db['Affected_Suppliers_List']
    cursor = collection_affected.find({})
    real_estate_affected_list = []
    for document in cursor:
        if supplier == document['企业名称']:
            real_estate_affected_list.append(document)
    return real_estate_affected_list


# 查询预测
def search_supplier_forecast(supplier):
    supplier_revenue = []
    supplier_profit = []
    supplier_cash_flow = []
    supplier_ROE = []
    collection = db['Financial_Data_Supplier']
    documents = collection.find({'Company': supplier['供应商']})

    for document in documents:
        supplier_revenue.append({
            'year': document['Date'],
            'value': document['NOI']
        })
        supplier_profit.append({
            'year': document['Date'],
            'value': document['Net_Profit']
        })
        supplier_cash_flow.append({
            'year': document['Date'],
            'value': document['Net_Cash_Flows_from_Operating_Activities']
        })
        supplier_ROE.append({
            'year': document['Date'],
            'value': document['ROE']
        })
    return supplier_revenue, supplier_profit, supplier_cash_flow, supplier_ROE


# 查询供应商自身风险
def search_supplier_affected(supplier):
    affected_degree = []
    supplier_collection = db['Financial_Data_Supplier']
    supplier_affect_degree = db['supplier_affected_data']

    supplier_one = supplier_collection.find_one({'Company': supplier['供应商']})
    supplier_affect_one = supplier_affect_degree.find_one({'供应商公司名': supplier['供应商']})
    if supplier_one is None or supplier_affect_one is None:
        return affected_degree
    denominator = supplier_affect_one['供应商来自房地产公司收入'] + supplier_affect_one['供应商总收入']
    if denominator != 0:
        degree_of_influence = round(
            supplier_affect_one['房地产对其应付账款'] / denominator,
            4
        )
    else:
        # 处理分母为零的情况，比如设置degree_of_influence为0或NaN
        degree_of_influence = 0  # 或者你可以使用float('nan')来表示不是一个数字
    reason = generate_affected_reason(supplier_one, degree_of_influence)
    affected_degree.append({
        'Date': supplier_one['Date'],
        'value': degree_of_influence,
        'reason': reason
    })
    # print(f'value:{degree_of_influence}')
    return affected_degree


# 非会员可查看页面
def search_supplier_nonmember(supplier):
    supplier = search_base_supplier(supplier)
    real_estate_list = []
    real_estate_affected_list = []
    error_message = None
    if supplier is not None:
        real_estate_list = search_real_estate_list_by_supplier(supplier['供应商'])
        real_estate_affected_list = search_real_estate_affected_list_by_supplier(supplier['供应商'])
    else:
        error_message = "未找到指定供应商"
    return supplier, real_estate_list, real_estate_affected_list, error_message


# 生成格式化数据，方便返回给前端
def generate_supplier_data_format(supplier, real_estate_list, real_estate_affected_list):
    testData1 = []
    riskCauseData = []
    affected_degree = []
    supplier_revenue = []
    supplier_profit = []
    supplier_cash_flow = []
    supplier_ROE = []
    if supplier is not None:
        affected_degree = search_supplier_affected(supplier)
        supplier_revenue, supplier_profit, supplier_cash_flow, supplier_ROE \
            = search_supplier_forecast(supplier)
        for real_estate in real_estate_list:
            real_estate_name = real_estate['企业名称']
            stock_code = real_estate['股票代码']
            # ... 可以继续添加其他需要的属性
            affection = '无影响'
            for real_estate_affected in real_estate_affected_list:
                real_estate_affected_name = real_estate_affected.get('房地产公司名称')
                if real_estate_affected_name == real_estate_name:
                    affection = '有影响'
                    break  # 如果找到匹配项，跳出循环
            testData1.append({
                "realEstateName": real_estate_name,
                "realEstateCode": stock_code,
                "realEstateAffection": affection
            })
        for real_estate_affected in real_estate_affected_list:
            real_estate_affected_name = real_estate_affected['房地产公司名称']
            value = real_estate_affected['是否产生影响']
            riskCauseData.append({
                "value": value,
                "name": real_estate_affected_name
            })
    return testData1, riskCauseData, affected_degree, supplier_revenue, supplier_profit, supplier_cash_flow, supplier_ROE


if __name__ == "__main__":
    print(os.getcwd())
    supplier, real_estate_list, real_estate_affected_list, error_message = search_supplier_nonmember('08811970-X')
    print(supplier)
    print(real_estate_list)
    print(real_estate_affected_list)
    testData1, riskCauseData, affected_degree, supplier_revenue, supplier_profit, supplier_cash_flow, supplier_ROE = generate_supplier_data_format(supplier, real_estate_list, real_estate_affected_list)
    print(testData1)
    print(riskCauseData)
