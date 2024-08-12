# -*- coding: utf-8 -*-
import sys , os
sys.path.append(os.path.join(os.path.dirname(__file__), '../models'))
import pandas as pd
import numpy as np
import torch
import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from xgboost import XGBRegressor
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, mean_squared_error

from SupplierIAModel import SupplierIAModel

IA_data_source = '../../proprisk-data/data/cooked/supplier_affected_data.csv'

def evaluate_supplier_affected(url):
    """
    影响程度：
    恒大对某供应商应付账款/（恒大对某供应商应付账款+供应商总收入）
    """
    datasets = pd.read_csv(url)
    print(datasets)
    # 去除前两行
    datasets = datasets.iloc[:, :]
    degree_of_influence = pd.DataFrame
    if datasets['房地产对其应付账款'] is not None:
        degree_of_influence = datasets['房地产对其应付账款'].astype(float)\
                              /(datasets['供应商来自房地产公司收入'].astype(float)
                                +datasets['供应商总收入'].astype(float))
    print(degree_of_influence)
    return degree_of_influence


if __name__ == '__main__':
    d = evaluate_supplier_affected(IA_data_source)


