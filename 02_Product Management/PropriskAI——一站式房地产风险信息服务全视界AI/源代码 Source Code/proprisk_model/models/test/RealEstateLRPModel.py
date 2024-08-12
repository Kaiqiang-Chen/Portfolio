import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
import csv


# 定义神经网络模型
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hide_size, output_size):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hide_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hide_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x


# 加载数据集，假设数据集为data，包含11个特征和目标风险值
# 定义训练数据
data = ...


# 将数据分割为特征和目标
X = data[:, :11]  # 特征
y = data[:, 11]  # 目标风险值

# 定义神经网络模型参数
input_size = 11
hide_size = 64
output_size = 1

# 初始化神经网络模型
model_nn = NeuralNetwork(input_size, hide_size, output_size)

# 定义损失函数和优化器
criterion = nn.BCELoss()  # 二元交叉熵损失函数
optimizer_nn = optim.Adam(model_nn.parameters(), lr=0.001)

# 训练神经网络模型
num_epochs = 100
for epoch in range(num_epochs):
    # 将数据转换为张量
    inputs = torch.tensor(X, dtype=torch.float32)
    labels = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    # 前向传播
    outputs = model_nn(inputs)
    loss = criterion(outputs, labels)

    # 反向传播与优化
    optimizer_nn.zero_grad()
    loss.backward()
    optimizer_nn.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# 定义随机森林模型
model_rf = RandomForestClassifier()

# 训练随机森林模型
model_rf.fit(X, y)

# 定义XGBoost模型
model_xgb = XGBClassifier()

# 训练XGBoost模型
model_xgb.fit(X, y)

# 定义投票分类器
models = [('rf', model_rf), ('xgb', model_xgb)]
model_voting = VotingClassifier(models, voting='soft')

# 训练投票分类器
model_voting.fit(X, y)


# 定义预测函数
def predict_risk(features):
    # 对输入特征进行预处理
    features_tensor = torch.tensor(features, dtype=torch.float32)

    # 使用神经网络进行预测
    nn_output = model_nn(features_tensor).item()

    # 使用随机森林进行预测
    rf_output = model_rf.predict_proba([features])[0][1]

    # 使用XGBoost进行预测
    xgb_output = model_xgb.predict_proba([features])[0][1]

    # 使用投票分类器进行预测
    voting_output = model_voting.predict_proba([features])[0][1]

    # 将四种模型的预测结果加权平均作为最终预测结果
    final_output = (nn_output + rf_output + xgb_output + voting_output) / 4

    return final_output


# 示例输入
features_example = [0.5, 0.8, 0.6, 0.7, 0.3, 0.9, 0.4, 0.2, 0.6, 0.8, 0.5]
predicted_risk = predict_risk(features_example)
print(f"Predicted Risk Probability: {predicted_risk}")
