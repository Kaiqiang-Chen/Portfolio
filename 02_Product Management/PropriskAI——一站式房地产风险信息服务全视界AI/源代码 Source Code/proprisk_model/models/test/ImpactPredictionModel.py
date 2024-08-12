import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


# ����������ģ��
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


# ���ݼ�
# ��������һ����Ϊdataset��numpy���飬ÿ�д���һ�����ݵ㣬�����ĸ�ָ��Ͷ�Ӧ����Ӱ��̶�
# ���磬dataset[i] = [business_dependency, revenue_ratio, liquidity_ratio, quick_ratio, impact_degree]

# ģ�Ͳ���
input_size = 4
hidden_size = 8
output_size = 1
learning_rate = 0.001
num_epochs = 1000

# ����Ԥ����
# ����Ҫ�����ݻ���Ϊѵ�����Ͳ��Լ����Լ�����ת��ΪPyTorch����
# ����������Ѿ��������Щ����

# ����ģ�͡���ʧ�������Ż���
model = ImpactPredictionNN(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# ѵ��ģ��
for epoch in range(num_epochs):
    # �����ݴ���ģ�ͽ���ǰ�򴫲�
    outputs = model(inputs)
    loss = criterion(outputs, labels)  # ������ʧ

    # ���򴫲����Ż�
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # ÿ��һ��ʱ���ӡ��ʧ
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# ����ģ��
torch.save(model.state_dict(), 'impact_prediction_model.pth')

# ʹ��ģ�ͽ���Ԥ��
# ���ر����ģ��
model = ImpactPredictionNN(input_size, hidden_size, output_size)
model.load_state_dict(torch.load('impact_prediction_model.pth'))

# ����ģ��Ϊ����ģʽ
model.eval()

# �����Ԥ����ĸ�ָ��
input_data = torch.tensor([business_dependency_value, revenue_ratio_value, liquidity_ratio_value, quick_ratio_value],
                          dtype=torch.float32)

# ����Ԥ��
with torch.no_grad():
    output = model(input_data)
    predicted_impact_degree = output.item()
    print(f'Predicted Impact Degree: {predicted_impact_degree:.2f}')
