import pandas as pd  
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import StandardScaler  
from sklearn.metrics import mean_squared_error, r2_score  
import xgboost as xgb  
# 利润
# 读取数据并处理缺失值  
df = pd.read_csv('../data/data.csv', na_values=['-'])  
df = df.fillna(0)  
  
# 选择输入变量和目标变量  
X = df[['存货', '总负债', '总资产', '应收账款','营业收入','营业成本','营业利润','经营活动产生的现金流量净额']]  
y = df['净利润']  
  
# 数据标准化  
scaler = StandardScaler()  
X_scaled = scaler.fit_transform(X)  
  
# 划分数据集  
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)  
  
# 转换数据为DMatrix格式，这是XGBoost优化过的数据结构  
dtrain = xgb.DMatrix(X_train, label=y_train)  
dtest = xgb.DMatrix(X_test, label=y_test)  
  
# 设置XGBoost参数  
params = {  
    'objective': 'reg:squarederror',  # 回归问题  
    'max_depth': 3,                    # 树的最大深度  
    'eta': 0.085,                        # 学习率  
    'subsample': 1,                  # 随机采样训练样本比例  
    'colsample_bytree': 1,           # 随机采样特征比例  
    'eval_metric': 'rmse'               # 评估指标：均方根误差  
}  
  
# 训练模型  
num_round = 250  # 迭代次数  
bst = xgb.train(params, dtrain, num_round)  
  
# 预测  
# y_pred = bst.predict(dtest)  
# print([(round(x, 2), round(y, 2)) for x, y in zip(y_test, y_pred)])  
# print(len(y_pred))  
  
# 评估模型  
# mse = mean_squared_error(y_test, y_pred)  
# r2 = r2_score(y_test, y_pred)  
  
# print(f'Mean Squared Error: {mse}')  
# print(f'R2 Score: {r2}')
bst.save_model('profit_xgb.model')

'''
预测方法：
import pandas as pd  
import xgboost as xgb  
  
# 假设new_data是新数据集，它只包含特征，不包含标签  
df = pd.read_csv('new_data.csv')  # 读取新数据  
X = df[['存货', '总负债', '总资产', '应收账款','营业收入','营业成本','营业利润','经营活动产生的现金流量净额']]  
scaler = StandardScaler()  
X_scaled = scaler.fit_transform(X)  
  
# 将新数据转换为DMatrix格式，注意这里不传入label参数  
dnew = xgb.DMatrix(X_scaled)  
  
# 加载之前保存的模型  
loaded_model = xgb.Booster()  
loaded_model.load_model('./SavedModel/revenue_xgb.model')  
  
# 使用加载的模型进行预测  
y_pred = loaded_model.predict(dnew)  
  
# 打印预测结果  
print(y_pred) // 这会是一个包含所有数据的列表
'''