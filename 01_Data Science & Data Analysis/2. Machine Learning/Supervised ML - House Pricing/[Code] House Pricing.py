
import warnings
warnings.filterwarnings("ignore")   # 忽略警告信息

from scipy.stats import norm, skew  # 获取统计信息
from scipy import stats
import numpy as np
import pandas as pd    # 数据处理包
import seaborn as sns  # 绘图包
color = sns.color_palette()
sns.set_style('darkgrid')
import matplotlib.pyplot as plt 
from matplotlib.font_manager import FontProperties

# 定义字体
font = FontProperties(fname=r"C:\Windows\Fonts\SimHei.ttf", size=14)  # Windows下的字体路径


%matplotlib inline


pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))  # 限制浮点输出到小数点后3位

import os
print('\n'.join(os.listdir('./input')))  # 列出目录中可用的文件

# %% [markdown]
# ### 加载数据集

# %%
# 加载数据
train = pd.read_csv('./input/train.csv')
test = pd.read_csv('./input/test.csv')

# %%
# 查看样本和特征的数量
print(train.shape)
print(test.shape)

# %%
train.head(5)

# %%
test.head(5)

# %%
# 保存Id列
train_ID = train['Id']
test_ID = test['Id']

# 删除原数据集的Id列
train.drop("Id", axis=1, inplace=True)
test.drop("Id", axis=1, inplace=True)

# %% [markdown]
# ### 数据预处理和特征工程

# %% [markdown]
# 异常值处理；目标变量分析；缺失值处理；特征相关性；进一步挖掘特征；对特征进行Box-Cox变换；独热编码。

# %% [markdown]
# #### 异常值处理

# %% [markdown]
# 通过绘制散点图可以直观地看出训练集特征是否有离群值，这里以地上生活面积 GrLivArea 为例。
# 我们可以看到，图像右下角的两个点有着很大的GrLivArea，但相应的SalePrice却异常地低，我们有理由相信它们是离群值，要将其剔除。

# %%
plt.figure(figsize=(14, 4))

plt.subplot(121)
plt.scatter(x=train['GrLivArea'], y=train['SalePrice'])
plt.ylabel('SalePrice', fontsize=13)
plt.xlabel('GrLivArea', fontsize=13)

train = train.drop(train[(train['GrLivArea'] > 4000) & (train['SalePrice'] < 300000)].index)
plt.subplot(122)
plt.scatter(train['GrLivArea'], train['SalePrice'])
plt.ylabel('SalePrice', fontsize=13)
plt.xlabel('GrLivArea', fontsize=13)


fig, ax = plt.subplots(nrows=2, figsize=(6, 10))
sns.distplot(train['SalePrice'], fit=norm, ax=ax[0])
(mu, sigma) = norm.fit(train['SalePrice'])
ax[0].legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)], loc='best')
ax[0].set_ylabel('Frequency')
ax[0].set_title('SalePrice distribution')
# QQ图
stats.probplot(train['SalePrice'], plot=ax[1])
plt.show()

# %% [markdown]
# 可以看到，SalePrice的分布呈正偏态，而线性回归模型要求因变量服从正态分布。我们**对其做对数变换**，让数据接近正态分布。

# %%
# 使用numpy中函数log1p()将log(1+x)应用于列的所有元素
train["SalePrice"] = np.log1p(train["SalePrice"])

# 查看转换后数据分布
# 分布图
fig, ax = plt.subplots(nrows=2, figsize=(6, 10))
sns.distplot(train['SalePrice'], fit=norm, ax=ax[0])
(mu, sigma) = norm.fit(train['SalePrice'])
ax[0].legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(
    mu, sigma)], loc='best')
ax[0].set_ylabel('Frequency')
ax[0].set_title('SalePrice distribution')

# QQ图
stats.probplot(train['SalePrice'], plot=ax[1])
plt.show()

# %% [markdown]
# 正态分布的数据有很多好的性质，使得后续的模型训练有更好的效果。另一方面，由于这次比赛最终是对预测值的对数的误差进行评估，所以我们在本地测试的时候也应该用同样的标准。

# %% [markdown]
# #### 缺失值处理

# %% [markdown]
# 1. 首先将训练集和测试集合并在一起

# %%
all_data = pd.concat((train, test)).reset_index(drop=True)
all_data.drop(['SalePrice'], axis=1, inplace=True)

print("all_data size is : {}".format(all_data.shape)) # print(f"all_data size is : {all_data.shape}")

# %% [markdown]
# 2. 统计各个特征的缺失情况

# %%
all_data_na = (all_data.isnull().sum() / len(all_data)) * 100
all_data_na


# %%
all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False) 
missing_data = pd.DataFrame({'Missing Ratio': all_data_na})
missing_data.head(10)

# %%
missing_data.shape[0]

# %%
fig, ax = plt.subplots(figsize=(15, 8))
barplot = sns.barplot(x=all_data_na.values, y=all_data_na.index, ax=ax)
sns.barplot(x=all_data_na, y=all_data_na.index)
plt.xticks(rotation=90)
plt.ylabel('变量名', fontsize=15,fontproperties=font)
plt.xlabel('缺失数据占比 (%)', fontsize=15,fontproperties=font)
plt.title('不同变量的缺失数据占比', fontsize=15,fontproperties=font)
for container in barplot.containers:
    barplot.bar_label(container, fmt='%.2f%%')

# %% [markdown]
# 3. 填补缺失值

# %% [markdown]
# 在data_description.txt中已有说明，一部分特征值的缺失是因为这些房子根本没有该项特征，对于这种情况我们统一用“None”或者“0”来填充。\
# Python中的None是一个特殊常量，不是0，也不是False，不是空字符串，更多的是表示一种不存在，是真正的空。它就是一个空的对象，只是没有赋值而已。
# 

# %% [markdown]
# - **PoolQC** : 数据描述说 NA 表示“没有泳池”。 这是有道理的，因为大多数房子一般都没有游泳池，因而缺失值的比例很高（+99%）。
# - **MiscFeature** : 数据描述说 NA 表示“没有杂项”。
# - **Alley** : 数据描述NA 表示“没有小巷通往”。
# - **Fence** : 数据描述说 NA 表示“没有围栏”。
# - **FireplaceQu** : 数据描述说 NA 的意思是“没有壁炉”。
# ......

# %%
# 用None或0填补25个含缺失值特征
all_data["PoolQC"] = all_data["PoolQC"].fillna("None")
all_data["MiscFeature"] = all_data["MiscFeature"].fillna("None")
all_data["Alley"] = all_data["Alley"].fillna("None")
all_data["Fence"] = all_data["Fence"].fillna("None")
all_data["FireplaceQu"] = all_data["FireplaceQu"].fillna("None")
all_data["MasVnrType"] = all_data["MasVnrType"].fillna("None")
all_data["MasVnrArea"] = all_data["MasVnrArea"].fillna(0)
for col in ('GarageType', 'GarageFinish', 'GarageQual', 'GarageCond'):
    all_data[col] = all_data[col].fillna('None')
for col in ('GarageYrBlt', 'GarageArea', 'GarageCars'):
    all_data[col] = all_data[col].fillna(0)
for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath'):
    all_data[col] = all_data[col].fillna(0)
for col in ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2'):
    all_data[col] = all_data[col].fillna('None')

# %% [markdown]
# 对于缺失较少的离散型特征，比如Electrical，可以用众数填补缺失值。 

# %%
# 用众数填补6个缺失较少的离散型特征缺失值
all_data['MSZoning'] = all_data['MSZoning'].fillna(all_data['MSZoning'].mode()[0])
all_data['Electrical'] = all_data['Electrical'].fillna(all_data['Electrical'].mode()[0])
all_data['KitchenQual'] = all_data['KitchenQual'].fillna(all_data['KitchenQual'].mode()[0])
all_data['Exterior1st'] = all_data['Exterior1st'].fillna(all_data['Exterior1st'].mode()[0])
all_data['Exterior2nd'] = all_data['Exterior2nd'].fillna(all_data['Exterior2nd'].mode()[0])
all_data['SaleType'] = all_data['SaleType'].fillna(all_data['SaleType'].mode()[0])

# %% [markdown]
# - **LotFrontage** : 由于房屋到街道的距离，最有可能与其附近其他房屋到街道的距离相同或相似，因此我们可以通过**该社区的 LotFrontage 中位数**来填充缺失值。

# %%
all_data["LotFrontage"] = all_data.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.median()))

# %% [markdown]
# - **Functional** : 居家功能性，数据描述说NA表示类型"Typ"。因此，我们用其填充。

# %%
all_data["Functional"] = all_data["Functional"].fillna("Typ")

# %% [markdown]
# - **Utilities** : 设备可用性，对于这个特征，所有记录除了一个“NoSeWa”和 2 个 NA ，其余值都是“AllPub”，因此该项特征的方差非常小。 并且带有“NoSewa”的房子在训练集中，也就是说测试集都是“AllPub”,这个特征对预测建模没有帮助。因此，我们可以安全地删除它。

# %%
all_data = all_data.drop(['Utilities'], axis=1)

# %% [markdown]
# 4. 最后确认缺失值是否已全部处理完毕

# %%
all_data.isnull().sum().max()

# %% [markdown]
# #### 特征相关性
# 
# **相关性矩阵热图**可以表现特征与目标值之间以及两两特征之间的相关程度，对特征的处理有指导意义。

# %%
train

# %%
# seaborn中函数heatmap()可以查看特征如何与 SalePrice 相关联
# corrmat = train.corr()
numerical_train = train.select_dtypes(include=[np.number])

# 计算相关性矩阵
corrmat = numerical_train.corr()
plt.figure(figsize=(12, 9))
sns.heatmap(corrmat, vmax=0.9, square=True)
plt.title('相关性热力图',fontproperties=font)

# %%
numerical_train.shape

# %%
saleprice_corr = corrmat['SalePrice'].sort_values(ascending=False)

# 打印与 'SalePrice' 相关性最高的五个特征（包括 'SalePrice' 自身）
top_features = saleprice_corr.head(6)  # 选取前六个因为第一个是 'SalePrice' 自身

print("与 'SalePrice' 相关性最高的五个特征:")
print(top_features[1:])  # 排除 'SalePrice' 自身


# %%
high_corr = (corrmat.where(np.triu(np.abs(corrmat) > 0.8, k=1))
                    .stack()
                    .reset_index())
high_corr.columns = ['feature1', 'feature2', 'correlation']
print(high_corr)
# 筛选出相关性高于0.8的特征
features = np.unique(high_corr[['feature1', 'feature2']].values)
sub_corrmat = corrmat.loc[features, features]

# 绘制热力图
plt.figure(figsize=(12, 9))
sns.heatmap(sub_corrmat, annot=True, cmap='coolwarm', vmax=1.0, vmin=-1.0, square=True, cbar_kws={"shrink": .82})
font = FontProperties(fname=r"C:\Windows\Fonts\SimHei.ttf", size=14)  # 根据实际情况修改字体路径
plt.title('相关性大于0.8的特征热力图', fontproperties=font)
plt.show()


# %% [markdown]
# #### 进一步挖掘特征

# %% [markdown]
# 1. 转换部分数值特征为分类特征
# 
# 我们注意到有些特征虽然是数值型的，但其实表征的只是不同类别，其数值的大小并没有实际意义，因此我们将其转化为分类特征。
# - **MSSubClass**   住宅标识
# - **YrSold**  开售年份
# - **MoSold**  开售月份

# %%
all_data['MSSubClass'] = all_data['MSSubClass'].apply(str)  # apply()函数默认对列进行操作
all_data['YrSold'] = all_data['YrSold'].astype(str)
all_data['MoSold'] = all_data['MoSold'].astype(str)

# %% [markdown]
# 2. 转换部分分类特征为数值特征
# 
# 反过来，有些类别特征实际上有高低好坏之分，这些特征的质量越高，就可能在一定程度导致房价越高。\
# 我们将这些特征的类别映射成有大小的数字，以此来表征这种潜在的偏序关系。**（标签编码LabelEncoder）**
# - **PoolQC**  泳池质量，有Ex	Excellent（优秀）Gd	Good（良好） 等等

# %%
from sklearn.preprocessing import LabelEncoder
cols = ('FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual', 'GarageCond',
        'ExterQual', 'ExterCond', 'HeatingQC', 'PoolQC', 'KitchenQual', 'BsmtFinType1',
        'BsmtFinType2', 'Functional', 'Fence', 'BsmtExposure', 'GarageFinish', 'LandSlope','LotShape', 
        'PavedDrive', 'Street', 'Alley', 'CentralAir', 'MSSubClass', 'OverallCond','YrSold', 'MoSold')

# 处理列，将标签编码应用于分类特征
for c in cols:
    lbl = LabelEncoder()   
    lbl.fit(list(all_data[c].values))
    all_data[c] = lbl.transform(list(all_data[c].values))

print('Shape all_data: {}'.format(all_data.shape))

# %% [markdown]
# 3. 利用一些重要的特征构造更多的特征
# 
# - TotalBsmtSF：地下室总面积
# - 1stFlrSF：一层面积
# - 2ndFlrSF：二层面积
# - OverallQual：整体材料和装饰综合质量
# - GrLivArea：地上生活面积
# - TotRmsAbvGrd：地上总房间数
# - GarageArea：车库面积
# - YearBuilt：建造时间

# %%
# 构造更多的特征
all_data['TotalSF'] = all_data['TotalBsmtSF'] + all_data['1stFlrSF'] + all_data['2ndFlrSF'] # 房屋总面积

all_data['OverallQual_TotalSF'] = all_data['OverallQual'] * all_data['TotalSF']  # 整体质量与房屋总面积交互项
all_data['OverallQual_GrLivArea'] = all_data['OverallQual'] * all_data['GrLivArea'] # 整体质量与地上总房间数交互项
all_data['OverallQual_TotRmsAbvGrd'] = all_data['OverallQual'] * all_data['TotRmsAbvGrd'] # 整体质量与地上生活面积交互项
all_data['GarageArea_YearBuilt'] = all_data['GarageArea'] * all_data['YearBuilt'] # 车库面积与建造时间交互项

# %% [markdown]
# #### 对特征进行Box-Cox变换

# %% [markdown]
# 1. 对于数值型特征，我们希望它们尽量服从正态分布，也就是不希望这些特征出现正负偏态。那么我们先来计算一下各个特征的偏度：

# %%
# 筛选出所有数值型特征(63个)
numeric_feats = all_data.dtypes[all_data.dtypes != "object"].index  

# 计算特征的偏度
numeric_data = all_data[numeric_feats]
skewed_feats = numeric_data.apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
skewness = pd.DataFrame({'Skew' :skewed_feats})
skewness.head(10)

# 筛选偏度大于0.75的变量
high_skew_feats = skewness[skewness['Skew'] > 0.75]

# 绘制偏度大于0.75的变量的柱状图
plt.figure(figsize=(15, 10))
ax = sns.barplot(y=high_skew_feats.index, x=high_skew_feats['Skew'])
plt.yticks(rotation=0, fontproperties=font)
plt.xlabel('偏度', fontsize=15, fontproperties=font)
plt.ylabel('数值特征', fontsize=15, fontproperties=font)
plt.title('偏度大于0.75的数值特征的偏度', fontsize=15, fontproperties=font)

# 在每个柱子上显示数值
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f')



# %% [markdown]
# 2. 对高偏度的特征进行Box-Cox变换

# %%
new_skewness = skewness[skewness.abs() > 0.75]
print("有{}个高偏度特征被Box-Cox变换".format(new_skewness.shape[0]))

# %% [markdown]
# 使用 scipy 中 boxcox1p() 函数计算**\\(1 + x\\) 的 Box-Cox 变换** ，当\\( \lambda = 0 \\) 等效于目标变量的 log1p
# 
# 选出偏度绝对值大于0.75的数据；找出这些偏度对应的特征；将偏度平滑至0.15
# 

# %%
from scipy.special import boxcox1p

skewed_features = new_skewness.index 
lam = 0.15
for feat in skewed_features:
    all_data[feat] = boxcox1p(all_data[feat], lam)

# %% [markdown]
# #### 独热编码（one-hot encoding)

# %% [markdown]
# 上述主要是在处理数值型特征，接下来处理类别特征。
# 对于类别特征，我们将其转化为独热编码，既解决了模型不好处理属性数据的问题，在一定程度上也起到了扩充特征的作用。

# %%
df = pd.DataFrame({'color': ['红', '蓝', '黄']})
df

# %%
lbl = LabelEncoder()   
df['color'] = lbl.fit(list(df.values)).transform(list(df.values))
df

# %%
df = pd.DataFrame({'color': ['红', '蓝', '黄']})
pd.get_dummies(df)

# %%
all_data = pd.get_dummies(all_data)
print(all_data.shape)

# %% [markdown]
# ### 建立模型
# 

# %% [markdown]
# #### 导入算法包

# %%
from sklearn.linear_model import ElasticNet, Lasso
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import lightgbm as lgb

# %%
y_train = train.SalePrice.values
train = all_data[:train.shape[0]] #切分训练集和测试集
test = all_data[train.shape[0]:]

# %%
train_numerical = train.select_dtypes(include=[np.number])
train_numerical.shape

# %% [markdown]
# #### 评价函数

# %% [markdown]
# 先定义一个评价函数。采用5折交叉验证。根据比赛评价标准，用Root-Mean-Squared-Error (RMSE)来为每个模型打分。
# 
# 使用sklearn中的cross_val_score()函数，但是这个函数没有 shuffle 属性，所以添加一行代码，在交叉验证之前对数据集进行 shuffle。
# 
# shuffle=True就表示对数据打乱，重新洗牌，这样就能设置随机种子。

# %%
n_folds = 5
def rmsle_cv(model):
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(train.values)
    rmse = np.sqrt(-cross_val_score(model, train_numerical.values, y_train, scoring="neg_mean_squared_error", cv=kf))
    return(rmse)

# %% [markdown]
# #### 基本模型

# %% [markdown]
# -  **LASSO Regression（套索回归）**  
# 

# %% [markdown]
# lasso回归就是在传统的线性回归目标函数后面加上了一个L1-范数，也称为为L1正则项，这样就能使得不重要特征的系数压缩至0，从而实现较为准确的参数估计效果，但是该模型可能对异常值非常敏感，由于数据集中依然存在一定的离群点，所以我们sklearn中的RobustScaler对数据进行标准化处理。

# %%
lasso = make_pipeline(RobustScaler(), Lasso(alpha=0.0005, random_state=1))

# %% [markdown]
# - **Kernel Ridge Regression（核岭回归）** 
# 
# 还有一种压缩估计的方法叫岭回归，它通过在目标函数后加上一个L2正则项，同样达到防止过拟合的作用。 \
# 核岭回归是先对数据作核变换以适应各种非线性情形,然后再对数据作岭回归的一种模型。

# %%
KRR = KernelRidge(alpha=0.6, kernel='polynomial', degree=2, coef0=2.5)

# %% [markdown]
# - **ElasticNet Regression（弹性网络）** 
# 
# 当多个特征存在相关时，Lasso回归可能只会随机选择其中一个，岭回归则会选择所有的特征。如果将这两种正则化的方法结合起来，就能够集合两种方法的优势，这种正则化后的算法就被称为弹性网络回归。

# %%
ENet = make_pipeline(RobustScaler(), ElasticNet(alpha=0.0005, l1_ratio=.9, random_state=3))

# %% [markdown]
# - **Gradient Boosting Regression（梯度提升回归GBRT）**
# 

# %% [markdown]
# 梯度提升回归树(GBRT)算法是以CART回归树为基学习器的集成学习模型，通过迭代多棵回归树生成多个弱模型，然后将每个弱模型的预测结果相加，通过不断减小损失函数的值来调整模型。与其他集成学习算法相比，梯度提升回归树对参数设置更为敏感。

# %%
GBoost = GradientBoostingRegressor(n_estimators=3000, learning_rate=0.05,
                                   max_depth=4, max_features='sqrt',
                                   min_samples_leaf=15, min_samples_split=10,
                                   loss='huber', random_state=5) # 设置hue loss使其对异常值具有鲁棒性

# %% [markdown]
# - **XGBoost（极致梯度回归）** 

# %% [markdown]
# 极致梯度提升（XGBoost）是基于GBRT的一种改进算法，通过引入模型复杂度重新构造目标函数，在迭代每一棵树的过程中都力求最小化，同时最小化了模型的损失函数即损失率和模型的复杂度，从而来提高算法的运算效率。

# %%
model_xgb = xgb.XGBRegressor(colsample_bytree=0.5, gamma=0.05,
                             learning_rate=0.05, max_depth=3,
                             min_child_weight=1.8, n_estimators=2200,
                             reg_alpha=0.5, reg_lambda=0.8,
                             subsample=0.5, random_state=7, nthread=-1)

# %% [markdown]
# - **LightGBM** 

# %% [markdown]
# LightGBM也是基于GBRT算法的一种优化改进， \
# 其改进之一是采用了基于直方图的决策层树算法，对每个特征的取值做分段函数，将所有样本在该特征上的取值划分到某一段中，最终把特征取值离散化；\
# 改进之二是采用Leaf-wise的生长策略，使增益高的节点优先生长，从而减少低增益点浪费计算资源的问题，提高计算效率。 

# %%
model_lgb = lgb.LGBMRegressor(objective='regression', num_leaves=5,
                              learning_rate=0.05, n_estimators=720,
                              max_bin=55, bagging_fraction=0.8,
                              bagging_freq=5, feature_fraction=0.2,
                              feature_fraction_seed=9, bagging_seed=9,
                              min_data_in_leaf=6, min_sum_hessian_in_leaf=11, verbose=-1)

# %% [markdown]
# **模型效果评价**

# %% [markdown]
# 让我们通过评估交叉验证 RMSE 的均值和标准差来看看这些基础模型的表现

# %% [markdown]
# 五种基础模型

# %%
models = {'LinearRegression':linear,'Lasso': lasso, 'ElasticNet': ENet, 'Kernel Ridge': KRR,'SVM':svm_sigmoid}
results=[]
for model_name, model in models.items():
    score = rmsle_cv(model)
    results.append([model_name, round(score.mean(),4), score.std()])

# 创建 DataFrame
df_results = pd.DataFrame(results, columns=['Model', 'Mean Score', 'Std Dev'])

df_sorted = df_results.sort_values(by='Mean Score', ascending=True)
pd.set_option('display.float_format', '{:.4f}'.format)
# 显示排序后的结果
print("Sorted Results:")
print(df_sorted)

# %% [markdown]
# svm参数比较

# %%
models = {'SVM_rbf':svm_rbf, 'SVM_sigmoid':svm_sigmoid,'svm_linear':svm_linear}
results=[]
for model_name, model in models.items():
    score = rmsle_cv(model)
    results.append([model_name, round(score.mean(),4), score.std()])

# 创建 DataFrame
df_results = pd.DataFrame(results, columns=['Model', 'Mean Score', 'Std Dev'])

df_sorted = df_results.sort_values(by='Mean Score', ascending=True)
pd.set_option('display.float_format', '{:.4f}'.format)
# 显示排序后的结果
print("Sorted Results:")
print(df_sorted)

# %%


# %%
models = {'LinearRegression':linear,'Lasso': lasso, 'ElasticNet': ENet, 'Kernel Ridge': KRR,  'SVM':svm_sigmoid,
          'Gradient Boosting': GBoost, 'XGBoost': model_xgb, 'LightGBM': model_lgb,'RandomForest':rf}
results=[]
for model_name, model in models.items():
    score = rmsle_cv(model)
    results.append([model_name, round(score.mean(),4), score.std()])

# 创建 DataFrame
df_results = pd.DataFrame(results, columns=['Model', 'Mean Score', 'Std Dev'])

df_sorted = df_results.sort_values(by='Mean Score', ascending=True)
pd.set_option('display.float_format', '{:.4f}'.format)
# 显示排序后的结果
print("Sorted Results:")
print(df_sorted)

# %% [markdown]
# ### Bagging

# %%
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingRegressor
linear=linear_model.LinearRegression()

from sklearn.neighbors import KNeighborsRegressor
knn = KNeighborsRegressor(n_neighbors=5)

rf=RandomForestRegressor(n_estimators=l00, #决策树的数量
                         max_depth=None,#树的最大深度
                         min_samples_split=2,#拆分内部节点所需的最小样本数
                         random_state=42)#随机种子以确保重现性
bagging_lasso = BaggingRegressor(base_estimator=lasso,
                                 n_estimators=25,#使用25个1asso模型
                                 max_samples=0.5,#每个模型使用50%的数据,
                                 max_features=0.8,#每个模型使用8g%的特征,
                                 random_state=42)
#随机种子以确保重现性
bagging_xgb = BaggingRegressor(base_estimator=model_xgb,
                               n_estimators=25,#使用25个KGBoost模型
                               max_samples=0.5,#每个模型使用50%的数据
                               max_features=0.8,#每个模型使用80%的特征
                               random_state=42)#随机种子以确保重现性

# %%
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# 训练模型
rf_regressor.fit(train_numerical.values, y_train)

feature_importances = rf_regressor.feature_importances_

# 创建特征和其重要性的DataFrame
importances_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': feature_importances
})

# 对特征重要性进行排序
importances_df = importances_df.sort_values(by='Importance', ascending=False)

# 显示特征重要性
print(importances_df)

# %%
results = []

for model_name, model in models.items():
    score = rmsle_cv(model)
    results.append([model_name, round(score.mean(),4), score.std()])

# 创建 DataFrame
df_results = pd.DataFrame(results, columns=['Model', 'Mean Score', 'Std Dev'])

df_sorted = df_results.sort_values(by='Mean Score', ascending=True)

# 显示排序后的结果
print("Sorted Results:")
print(df_sorted)

# %% [markdown]
# #### 堆叠方法（[Stacking Models][1]）
# 
# [1]: https://www.jianshu.com/p/59313f43916f
# 

# %% [markdown]
# 集成学习往往能进一步提高模型的准确性，Stacking是其中一种效果颇好的方法，简单来说就是学习各个基本模型的预测值来预测最终的结果。

# %% [markdown]
# ![image-2.png](attachment:image-2.png)

# %% [markdown]
# 定义一个新类，表示Stacking方法

# %%
class StackingAveragedModels(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, base_models, meta_model, n_folds=5):
        self.base_models = base_models  # 第一层模型
        self.meta_model = meta_model    # 第二层模型
        self.n_folds = n_folds

    # 运用克隆的基本模型拟合数据
    def fit(self, X, y):
        self.base_models_ = [list() for x in self.base_models]
        self.meta_model_ = clone(self.meta_model)
        kfold = KFold(n_splits=self.n_folds, shuffle=True, random_state=156)

        # 训练克隆的第一层模型
        out_of_fold_predictions = np.zeros((X.shape[0], len(self.base_models)))
        for i, model in enumerate(self.base_models):
            for train_index, holdout_index in kfold.split(X, y):
                instance = clone(model)
                self.base_models_[i].append(instance)
                instance.fit(X[train_index], y[train_index])
                y_pred = instance.predict(X[holdout_index])
                out_of_fold_predictions[holdout_index, i] = y_pred

        # 使用交叉验证预测的结果作为新特征，来训练克隆的第二层模型
        self.meta_model_.fit(out_of_fold_predictions, y)
        return self

    # 在测试数据上做所有基础模型的预测，并使用平均预测作为由元模型完成的最终预测的元特征
    def predict(self, X):
        meta_features = np.column_stack([np.column_stack([model.predict(X) for model in base_models]).mean(axis=1) 
                                         for base_models in self.base_models_])
        return self.meta_model_.predict(meta_features)

# %% [markdown]
# 这里我们用ENet、KRR和GBoost作为第一层学习器，用Lasso作为第二层学习器。查看以下Stacking的交叉验证评分：

# %%
stacked_averaged_models = StackingAveragedModels(base_models=(ENet, GBoost, KRR), meta_model=lasso)

score = rmsle_cv(stacked_averaged_models)
print("Stacking Averaged models score: {:.4f} ({:.4f})".format(score.mean(), score.std()))

# %% [markdown]
# 

# %% [markdown]
# 我们得到了比单个基学习器更好的分数。

# %% [markdown]
# #### 建立最终模型

# %% [markdown]
# **集成StackedRegressor, XGBoost和 LightGBM**

# %% [markdown]
# **我们将XGBoost、LightGBM和StackedRegressor以加权平均的方式融合在一起，建立最终的预测模型**

# %% [markdown]
# 1. 首先，定义一个评价函数,表示预测值和实际值之间的均方根误差 RMSE

# %%
def rmsle(y, y_pred):
    return np.sqrt(mean_squared_error(y, y_pred))

# %% [markdown]
# 2. 其次，用整个训练集训练模型，预测测试集的房价，并给出模型在训练集上的评分

# %% [markdown]
# 注：numpy中的expm1()函数表示 \\(e^{x}-1\\)，即将预测的对数值转换为原始预测值

# %% [markdown]
# - **StackedRegressor:**

# %%
stacked_averaged_models.fit(train.values, y_train)
stacked_train_pred = stacked_averaged_models.predict(train.values)
stacked_pred = np.expm1(stacked_averaged_models.predict(test.values))  
print(rmsle(y_train, stacked_train_pred))

# %% [markdown]
# - **XGBoost:**

# %%
model_xgb.fit(train, y_train)
xgb_train_pred = model_xgb.predict(train)
xgb_pred = np.expm1(model_xgb.predict(test))
print(rmsle(y_train, xgb_train_pred))

# %% [markdown]
# - **LightGBM:**

# %%
model_lgb.fit(train, y_train)
lgb_train_pred = model_lgb.predict(train)
lgb_pred = np.expm1(model_lgb.predict(test.values))
print(rmsle(y_train, lgb_train_pred))

# %%
print('集成模型的得分:{}'.format(rmsle(y_train, stacked_train_pred*0.70 + xgb_train_pred*0.15 + lgb_train_pred*0.15)))

# %% [markdown]
# 3. 生成最终预测结果

# %%
ensemble = stacked_pred*0.70 + xgb_pred*0.15 + lgb_pred*0.15

# %% [markdown]
# #### 提交结果

# %%
sub = pd.DataFrame()
sub['Id'] = test_ID
sub['SalePrice'] = ensemble
sub.to_csv('submission.csv', index=False)
