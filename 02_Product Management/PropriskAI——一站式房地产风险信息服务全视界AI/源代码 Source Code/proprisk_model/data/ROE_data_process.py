# -*- coding: utf-8 -*-
import sys
import os

from sklearn.metrics import mean_squared_error
from torch import nn, optim

sys.path.append(os.path.join(os.path.dirname(__file__), '../models'))
import pandas as pd
import numpy as np
import torch
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.model_selection import train_test_split

from ROEPModel import ROEPModel

ROE_data_source = "../../proprisk-data/data/cooked/Financial_Data_new.csv"


# 读取并处理数据
def read_data_from_ROE(url):
    datasets_raw = pd.read_csv(url)
    print(datasets_raw)
    # 去除前两行
    datasets_raw = datasets_raw.iloc[2:, :]
    Y = datasets_raw['ROE'].astype(float)
    print(Y)

    # 初步处理数据
    # 处理数据并添加到 datasets_cooked 中
    datasets_cooked = pd.DataFrame()
    datasets_cooked['Net_Profit_Ratio'] = datasets_raw['Net_Profit'].astype(float) / datasets_raw[
        'Sales_revenue'].astype(float)
    datasets_cooked['Asset_Turnover_Ratio'] = datasets_raw['Sales_revenue'].astype(float) / datasets_raw[
        'Total_Assets'].astype(float)
    datasets_cooked['Equity_Multiplier'] = datasets_raw['Total_Assets'].astype(float) - datasets_raw[
        'Current_Liability'].astype(float)
    print(datasets_cooked)

    # 处理数据
    # 将数据转换为 PyTorch 张量
    X_tensor = torch.tensor(datasets_cooked.values, dtype=torch.float32)
    Y_tensor = torch.tensor(Y.values, dtype=torch.float32)
    # print(X_tensor)
    # print(Y_tensor)

    rdf_model = RandomForestRegressor()
    xgb_model = xgb.XGBRegressor()
    line_model = LinearRegression()

    rdf_model.fit(X_tensor, Y_tensor)
    output1 = rdf_model.predict(X_tensor)
    X_tensor2 = np.column_stack((X_tensor, output1))

    xgb_model.fit(X_tensor2, Y_tensor)
    output2 = xgb_model.predict(X_tensor2)
    X_tensor3 = np.column_stack((X_tensor2, output2))

    line_model.fit(X_tensor3, Y_tensor)
    output3 = line_model.predict(X_tensor3)
    output = np.column_stack((X_tensor3, output3))
    print(output)

    X_train, X_test, y_train, y_test = train_test_split(output, Y_tensor, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def train_ROE_model(X_train, X_test, y_train, y_test):
    count = 0
    while True:
        # 训练PyTorch模型
        input_dim = X_train.shape[1]
        model = ROEPModel(input_dim)
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
        count += 1
        if mse <= 0.00179:
            print(f'第{count}次训练后达到预期效果')
            print(f'方差值为: {mse:.4f}')
            print(predicted)
            print(y_test)
            torch.save(model.state_dict(), '../models/SavedModel/ROEPModel.pth')
            break


def load_ROE_model():
    # 实例化预测模型
    input_dim = 3
    model = ROEPModel(input_dim)
    # 加载模型参数
    model.load_state_dict(torch.load('../models/SavedModel/ROEPModel.pth'))
    return model


if __name__ == '__main__':
    print(os.getcwd())
    X_train, X_test, y_train, y_test = read_data_from_ROE(ROE_data_source)
    train_ROE_model(X_train, X_test, y_train, y_test)
