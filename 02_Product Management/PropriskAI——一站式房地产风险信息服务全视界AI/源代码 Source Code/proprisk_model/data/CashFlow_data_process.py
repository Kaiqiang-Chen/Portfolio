# -*- coding: utf-8 -*-
import sys
import os

from sklearn.metrics import mean_squared_error, r2_score
from torch import nn, optim

sys.path.append(os.path.join(os.path.dirname(__file__), '../models'))
import pandas as pd
import numpy as np
import torch
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.model_selection import train_test_split

from CashFlowPModel import CashFlowPModel

cash_flow_data_source = '../../proprisk-data/data/cooked/Financial_Data_new.csv'

# 读取处理数据
def read_cash_flow_data(url):
    datasets_raw = pd.read_csv(url)
    print(datasets_raw)
    # 去除前两行
    datasets_raw = datasets_raw.iloc[2:, :]
    datasets_raw = datasets_raw[datasets_raw['Net_Cash_Flows_from_Operating_Activities'] != '-']
    datasets_raw = datasets_raw[datasets_raw['Accounts_Receivable'] != '-']

    Y = datasets_raw['Net_Cash_Flows_from_Operating_Activities'].astype(float)
    print(Y)

    # 初步处理数据
    # 处理数据并添加到 datasets_cooked 中
    datasets_cooked = pd.DataFrame()
    datasets_cooked['Net_Profit'] = datasets_raw['Net_Profit'].astype(float)
    datasets_cooked['Accounts_Receivable'] = datasets_raw['Accounts_Receivable'].astype(float)
    datasets_cooked['Inventory'] = datasets_raw['Inventory'].astype(float)
    datasets_cooked['Accounts_Payable'] = datasets_raw['Accounts_Payable'].astype(float)

    X_tensor = torch.tensor(datasets_cooked.values, dtype=torch.float32)
    Y_tensor = torch.tensor(Y.values, dtype=torch.float32)

    return X_tensor, Y_tensor


def train_cash_flow_model(X_tensor, Y_tensor):
    dtrain = xgb.DMatrix(X_tensor, label=Y_tensor)

    # 设置XGBoost参数
    params = {
        'objective': 'reg:squarederror',
        'max_depth': 3,
        'eta': 0.001,
        'subsample': 1,
        'colsample_bytree': 1,
        'eval_metric': 'rmse'
    }

    epochs = 100
    cash_flow_model = xgb.train(params, dtrain, epochs)

    # 进行预测
    xgb_output = cash_flow_model.predict(dtrain)
    X_tensor2 = np.column_stack((X_tensor, xgb_output))

    X_train, X_test, y_train, y_test = \
        train_test_split(X_tensor2, Y_tensor, test_size=0.2, random_state=42)

    while True:
        # 训练PyTorch模型
        input_dim = X_train.shape[1]
        model = CashFlowPModel(input_dim)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        epochs = 100
        for epoch in range(epochs):
            model.train()
            optimizer.zero_grad()
            outputs = model(torch.FloatTensor(X_train))
            loss = criterion(outputs.squeeze(), torch.FloatTensor(y_train))
            # loss = criterion(outputs.squeeze(), torch.FloatTensor(y_train.values))
            loss.backward()
            optimizer.step()
            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

        # 模型评估
        model.eval()
        with torch.no_grad():
            predicted = model(torch.FloatTensor(X_test))
            # print(predicted)
            # print(y_test)
            # print(outputs)
            # predicted = outputs.round().numpy()

        # 计算均方误差
        mse = mean_squared_error(y_test, predicted)
        print(f'Mean Squared Error: {mse:.4f}')
        mse = mean_squared_error(y_test, predicted)
        torch.save(model.state_dict(), '../models/SavedModel/CashFlowPModel.pth')
        break



if __name__ == '__main__':
    print(os.getcwd())
    X_tensor, Y_tensor = read_cash_flow_data(cash_flow_data_source)
    train_cash_flow_model(X_tensor, Y_tensor)
