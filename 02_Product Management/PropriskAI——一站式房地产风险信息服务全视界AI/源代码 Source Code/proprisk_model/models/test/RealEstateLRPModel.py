import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
import csv


# ����������ģ��
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


# �������ݼ����������ݼ�Ϊdata������11��������Ŀ�����ֵ
# ����ѵ������
data = ...


# �����ݷָ�Ϊ������Ŀ��
X = data[:, :11]  # ����
y = data[:, 11]  # Ŀ�����ֵ

# ����������ģ�Ͳ���
input_size = 11
hide_size = 64
output_size = 1

# ��ʼ��������ģ��
model_nn = NeuralNetwork(input_size, hide_size, output_size)

# ������ʧ�������Ż���
criterion = nn.BCELoss()  # ��Ԫ��������ʧ����
optimizer_nn = optim.Adam(model_nn.parameters(), lr=0.001)

# ѵ��������ģ��
num_epochs = 100
for epoch in range(num_epochs):
    # ������ת��Ϊ����
    inputs = torch.tensor(X, dtype=torch.float32)
    labels = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    # ǰ�򴫲�
    outputs = model_nn(inputs)
    loss = criterion(outputs, labels)

    # ���򴫲����Ż�
    optimizer_nn.zero_grad()
    loss.backward()
    optimizer_nn.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# �������ɭ��ģ��
model_rf = RandomForestClassifier()

# ѵ�����ɭ��ģ��
model_rf.fit(X, y)

# ����XGBoostģ��
model_xgb = XGBClassifier()

# ѵ��XGBoostģ��
model_xgb.fit(X, y)

# ����ͶƱ������
models = [('rf', model_rf), ('xgb', model_xgb)]
model_voting = VotingClassifier(models, voting='soft')

# ѵ��ͶƱ������
model_voting.fit(X, y)


# ����Ԥ�⺯��
def predict_risk(features):
    # ��������������Ԥ����
    features_tensor = torch.tensor(features, dtype=torch.float32)

    # ʹ�����������Ԥ��
    nn_output = model_nn(features_tensor).item()

    # ʹ�����ɭ�ֽ���Ԥ��
    rf_output = model_rf.predict_proba([features])[0][1]

    # ʹ��XGBoost����Ԥ��
    xgb_output = model_xgb.predict_proba([features])[0][1]

    # ʹ��ͶƱ����������Ԥ��
    voting_output = model_voting.predict_proba([features])[0][1]

    # ������ģ�͵�Ԥ������Ȩƽ����Ϊ����Ԥ����
    final_output = (nn_output + rf_output + xgb_output + voting_output) / 4

    return final_output


# ʾ������
features_example = [0.5, 0.8, 0.6, 0.7, 0.3, 0.9, 0.4, 0.2, 0.6, 0.8, 0.5]
predicted_risk = predict_risk(features_example)
print(f"Predicted Risk Probability: {predicted_risk}")
