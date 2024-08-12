import torch
import torch.nn as nn
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error

# 模拟数据集
# 假设数据集中包含的特征数为11，其中前8个特征为features1，后3个特征为features2
# risk_radio 为目标
# 这里用随机数代替实际数据
num_samples = 1000
num_features1 = 8
num_features2 = 3
num_total_features = num_features1 + num_features2

features1 = np.random.rand(num_samples, num_features1)
features2 = np.random.rand(num_samples, num_features2)
risk_radio = np.random.rand(num_samples, 1)  # 假设这是目标

# 构建模型
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.layer1 = nn.Linear(num_features1, 1)
        self.layer2 = nn.Linear(num_total_features, 1)

    def forward(self, x1, x2):
        out1 = torch.sigmoid(self.layer1(x1))
        out2 = torch.sigmoid(self.layer2(torch.cat((x1, x2), dim=1)))
        return out1, out2

# 将数据转换为 PyTorch 张量
features1_tensor = torch.tensor(features1, dtype=torch.float32)
features2_tensor = torch.tensor(features2, dtype=torch.float32)
risk_radio_tensor = torch.tensor(risk_radio, dtype=torch.float32)

# 初始化模型
model = Model()

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练模型第三层
num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs1, outputs2 = model(features1_tensor, features2_tensor)
    loss1 = criterion(outputs1, risk_radio_tensor)
    loss2 = criterion(outputs2, risk_radio_tensor)
    loss = loss1 + loss2
    loss.backward()
    optimizer.step()
    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss1: {loss1.item():.4f}, Loss2: {loss2.item():.4f}')

# 获取第三层输出
features3_tensor = torch.cat((outputs1, outputs2), dim=1)

# 将 features3 转换为 numpy 数组
features3 = features3_tensor.detach().numpy()

# 将 F1 和 F2 加入到 features3 中
features4 = np.concatenate((features1, features2, risk_radio), axis=1)

# 使用 RDF 进行预测
rdf_model = RandomForestClassifier()
rdf_model.fit(features4, risk_radio.ravel())  # 拟合模型

# 使用 XGBoost 进行预测
xgb_model = xgb.XGBClassifier()
xgb_model.fit(features4, risk_radio.ravel())  # 拟合模型

# 在调整模型时，计算不同参数模型情况下 risk_radio 与 risk_radio_predict 之间的方差
# 略

# 假设最优模型为 RDF
# 使用最优模型进行预测
risk_radio_predict_rdf = rdf_model.predict(features4)

# 假设最优模型为 XGBoost
# 使用最优模型进行预测
risk_radio_predict_xgb = xgb_model.predict(features4)
