# -*- coding: utf-8 -*-

# Supplier impact assessment

import torch
import torch.nn as nn
# 定义SupplierIAModel模型 评估供应商受影响程度
class SupplierIAModel(nn.Module):
    def __init__(self, input_dim):
        super(SupplierIAModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x
