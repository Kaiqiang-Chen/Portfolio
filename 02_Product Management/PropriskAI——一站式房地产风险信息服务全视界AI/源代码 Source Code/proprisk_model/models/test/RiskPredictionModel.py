import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.model_selection import train_test_split

# 定义神经网络模型
class RiskPredictionModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RiskPredictionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.sigmoid(out)
        return out

# 数据预处理
def preprocess_data(data):
    # 对数据进行归一化处理
    normalized_data = (data - np.mean(data, axis=0)) / np.std(data, axis=0)
    return normalized_data

# 准备数据集
# 这里假设你已经有一个数据集，其中X包含11个指标，Y是对应的风险值
# 假设X和Y是numpy数组
X = np.random.rand(100, 11)  # 这里使用随机数据作为示例
Y = np.random.rand(100, 1)    # 这里使用随机数据作为示例

# 数据预处理
X = preprocess_data(X)

# 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 将数据转换为PyTorch张量并移动到CUDA上
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
Y_train_tensor = torch.tensor(Y_train, dtype=torch.float32).to(device)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
Y_test_tensor = torch.tensor(Y_test, dtype=torch.float32).to(device)

# 定义模型参数并将模型移动到CUDA上
input_size = 11
hidden_size = 64
output_size = 1
model = RiskPredictionModel(input_size, hidden_size, output_size).to(device)

# 定义损失函数和优化器
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练模型
num_epochs = 1000
for epoch in range(num_epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, Y_train_tensor)

    # Backward and optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))

# 在测试集上评估模型
with torch.no_grad():
    model.eval()
    outputs = model(X_test_tensor)
    predicted_risk = outputs.cpu().numpy()  # 将预测结果移回CPU

    # 计算准确率等评估指标
    # 这里可以根据具体情况添加评估指标的计算代码
    # 计算方差
    # variance = np.var(predicted_risk)
    # print("Variance on test set:", variance)

# 使用模型进行预测
# 假设predict_data是具体的11个指标的值，形状为(1, 11)
predict_data = np.random.rand(1, 11)  # 这里使用随机数据作为示例
predict_data = preprocess_data(predict_data)
predict_data_tensor = torch.tensor(predict_data, dtype=torch.float32).to(device)
with torch.no_grad():
    model.eval()
    output = model(predict_data_tensor)
    predicted_risk_probability = output.item()
    print("Predicted risk probability:", predicted_risk_probability)
