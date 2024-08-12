import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


# 定义神经网络模型
class ImpactPredictionNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ImpactPredictionNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return out


# 数据集
# 假设你有一个名为dataset的numpy数组，每行代表一个数据点，包含四个指标和对应的受影响程度
# 例如，dataset[i] = [business_dependency, revenue_ratio, liquidity_ratio, quick_ratio, impact_degree]

# 模型参数
input_size = 4
hidden_size = 8
output_size = 1
learning_rate = 0.001
num_epochs = 1000

# 数据预处理
# 你需要将数据划分为训练集和测试集，以及将其转换为PyTorch张量
# 这里假设你已经完成了这些步骤

# 定义模型、损失函数和优化器
model = ImpactPredictionNN(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 训练模型
for epoch in range(num_epochs):
    # 将数据传入模型进行前向传播
    outputs = model(inputs)
    loss = criterion(outputs, labels)  # 计算损失

    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 每隔一段时间打印损失
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# 保存模型
torch.save(model.state_dict(), 'impact_prediction_model.pth')

# 使用模型进行预测
# 加载保存的模型
model = ImpactPredictionNN(input_size, hidden_size, output_size)
model.load_state_dict(torch.load('impact_prediction_model.pth'))

# 设置模型为评估模式
model.eval()

# 输入待预测的四个指标
input_data = torch.tensor([business_dependency_value, revenue_ratio_value, liquidity_ratio_value, quick_ratio_value],
                          dtype=torch.float32)

# 进行预测
with torch.no_grad():
    output = model(input_data)
    predicted_impact_degree = output.item()
    print(f'Predicted Impact Degree: {predicted_impact_degree:.2f}')
