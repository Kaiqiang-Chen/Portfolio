# -*- coding: utf-8 -*-

import os
import argparse
import pytorch_lightning as pl
import torch
import numpy as np
from pytorch_lightning.utilities import seed
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import LearningRateMonitor, ModelCheckpoint, Timer
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks import RichProgressBar
from pytorch_lightning.callbacks.progress.rich_progress import RichProgressBarTheme
from pytorch_lightning.strategies import DDPStrategy
import pdb

from data.LRP_data_process import read_data_from_caiwubaogao
from data.LRP_data_process import train_LRP_model
from proprisk_model.data.CashFlow_data_process import read_cash_flow_data, train_cash_flow_model
from proprisk_model.data.ROE_data_process import read_data_from_ROE, train_ROE_model

LRP_data_source = "..\proprisk-data\data\cooked\caiwubaogao\Real_Estate_LRP_data.csv"
ROE_data_source = "..\proprisk-data\data\cooked\FFinancial_Data_new.csv"
cash_flow_data_source = '../proprisk-data/data/cooked/Financial_Data_new.csv'


def built_model():
    print('建立训练房地产流动性危机预测模型...')
    X_train, X_test, y_train, y_test = read_data_from_caiwubaogao(LRP_data_source)
    train_LRP_model(X_train, X_test, y_train, y_test)
    print('房地产流动性危机评估预测模型建立完成!')

    print('建立ROE预测模型...')
    X_train, X_test, y_train, y_test = read_data_from_ROE(ROE_data_source)
    train_ROE_model(X_train, X_test, y_train, y_test)
    print('ROE模型建立完成!')

    print('建立现金流预测模型...')
    X_tensor, Y_tensor = read_cash_flow_data(cash_flow_data_source)
    train_cash_flow_model(X_tensor, Y_tensor)
    print('现金流模型建立完成!')


if __name__ == '__main__':
    print(os.getcwd())
    print('建立模型...')
    built_model()
