import os, sys
from random import random, randint
from flask_cors import CORS
from flask import Flask, request, jsonify
from pymongo import MongoClient

# from mapper.supplier_data import search_base_supplier_by_name
# from util.chatUtil import generate_LRP_introduction
from proprisk.mapper.supplier_data import search_base_supplier_by_name
from proprisk.util.chatUtil import generate_LRP_introduction

client = MongoClient('mongodb://localhost:27017/')
db = client['gongyingshang']


# 查询房地产公司基本信息
def search_base_real_estate(realEstate):
    collection = db['company_information']
    cursor = collection.find({})
    for document in cursor:
        if realEstate == document['企业名称'] or realEstate == document['股票代码']:
            return document
    return None


# 查询房地产公司对应的造成影响的供应商
def search_supplier_list_impacted(realEstate):
    collection = db['Affected_Suppliers_List']
    cursor = collection.find({})
    impacted_suppliers_list = []
    for document in cursor:
        if realEstate == document['房地产公司名称']:
            impacted_suppliers_list.append(document)
    return impacted_suppliers_list


# 查询房地产公司流动性危机
def search_real_estate_LR(realEstate):
    collection = db['Real_Estate_LRP_data']
    cursor = collection.find_one({'Stock Code': realEstate['股票代码']})
    LR_reason = generate_LRP_introduction(cursor)
    return cursor['Date'], cursor['Risk_Radio'], LR_reason


# 预测查询
def search_forecast(realEstate):
    real_estate_revenue = []
    real_estate_profit = []
    real_estate_cash_flow = []
    real_estate_ROE = []
    collection = db['Financial_Data_new']
    documents = collection.find({'Stock_Code': realEstate['股票代码']})

    for document in documents:
        real_estate_revenue.append({
            'year': document['Date'],
            'value': document['NOI']
        })
        real_estate_profit.append({
            'year': document['Date'],
            'value': document['Net_Profit']
        })
        real_estate_cash_flow.append({
            'year': document['Date'],
            'value': document['Net_Cash_Flows_from_Operating_Activities']
        })
        real_estate_ROE.append({
            'year': document['Date'],
            'value': document['ROE']
        })
    return real_estate_revenue, real_estate_profit, real_estate_cash_flow, real_estate_ROE


# 非会员可查看页面
def search_real_estate_nonmember(realEstate):
    real_estate = search_base_real_estate(realEstate)
    impacted_suppliers_list = []
    impacted_suppliers_info_list = []
    error_message = None

    if real_estate is None:
        error_message = "未找到指定的房地产公司"
    else:
        impacted_suppliers_list = search_supplier_list_impacted(real_estate['企业名称'])
        for impacted_supplier in impacted_suppliers_list:
            impacted_suppliers_info_list.append(
                search_base_supplier_by_name(impacted_supplier['房地产公司名称'], impacted_supplier['企业名称']))

    return real_estate, impacted_suppliers_list, impacted_suppliers_info_list, error_message


# 生成指定数据格式 方便数据返回给前端页面展示
def generate_data_format(real_estate, impacted_suppliers_list, impacted_suppliers_info_list):
    testData = []
    riskCauseData = []
    LR_radio = []
    real_estate_revenue = []
    real_estate_profit = []
    real_estate_cash_flow = []
    real_estate_ROE = []
    if real_estate is not None:
        # 确保impacted_suppliers_list和impacted_suppliers_info_list具有相同数量的元素
        if len(impacted_suppliers_list) == len(impacted_suppliers_info_list):
            for supplier, info in zip(impacted_suppliers_list, impacted_suppliers_info_list):
                supplier_name = supplier.get('企业名称', '')  # 获取企业名称，如果键不存在，则默认为空字符串
                supplier_code = info.get('组织机构代码', '')  # 获取组织机构代码，如果键不存在，则默认为空字符串
                supplier_affection = supplier.get('是否产生影响', '')
                supplier_source_basis = supplier.get('依据', '')
                supplier_source_url = supplier.get('出处来源', '')
                testData.append({
                    "supplierName": supplier_name,
                    "supplierCode": supplier_code,
                    "supplierAffection": supplier_affection,
                    "sourceBasis": supplier_source_basis,
                    "sourceUrl": supplier_source_url
                })
                riskCauseData.append({
                    "value": randint(0, 100),  # 获取流动性危机爆发概率
                    "name": supplier_name
                })
        date, value, LR_reason = search_real_estate_LR(real_estate)
        LR_radio.append({
            "year": date,
            "value": value,
            "reason": LR_reason
        })
        real_estate_revenue, real_estate_profit, real_estate_cash_flow, real_estate_ROE\
            = search_forecast(real_estate)
    return testData, riskCauseData, LR_radio, real_estate_revenue, \
            real_estate_profit, real_estate_cash_flow, real_estate_ROE


if __name__ == "__main__":
    real_estate, impacted_suppliers_list, impacted_suppliers_info_list, error_message = \
        search_real_estate_nonmember('碧桂园地产集团有限公司')
    # print(real_estate)
    # print(impacted_suppliers_list)
    # print(impacted_suppliers_info_list)
    testData, riskCauseData, LR_radio, real_estate_revenue, real_estate_profit, real_estate_cash_flow, real_estate_ROE \
        = generate_data_format(real_estate, impacted_suppliers_list, impacted_suppliers_info_list)
    print(testData)
    print(riskCauseData)
    print(LR_radio)
    print(real_estate_revenue)
    print(real_estate_profit)
    print(real_estate_cash_flow)
    print(real_estate_ROE)
