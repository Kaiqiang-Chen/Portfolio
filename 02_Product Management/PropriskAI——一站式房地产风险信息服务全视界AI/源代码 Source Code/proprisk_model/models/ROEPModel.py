# -*- coding: utf-8 -*-

# ROE predict

import torch
import torch.nn as nn
# 定义ROEPModel模型 评估供应商受影响程度
class ROEPModel(nn.Module):
    def __init__(self, input_dim):
        super(ROEPModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 16)
        self.fc2 = nn.Linear(16, 32)
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x
