**目录**
- [关于互动广告与静态广告转化率的A/B实验](#关于互动广告与静态广告转化率的ab实验)
  - [实验目标](#实验目标)
  - [指标选择](#指标选择)
  - [变量定义](#变量定义)
  - [假设检验](#假设检验)
  - [实验设计](#实验设计)
  - [随机抽样](#随机抽样)
  - [数据分析](#数据分析)
  - [结论](#结论)

## 关于互动广告与静态广告转化率的A/B实验

### 实验目标

本实验旨在评估互动广告是否能显著提高用户的转化率，相较于静态广告。

### 指标选择

* **北极星指标** ：转化率（Conversion Rate）

### 变量定义

* **控制变量** ：静态广告
* **实验变量** ：互动广告

### 假设检验

* **原假设 (H0)** ：互动广告的转化率小于或等于静态广告的转化率。
* **备择假设 (H1)** ：互动广告的转化率优于静态广告的转化率。

### 实验设计

* **随机化单元** ：用户
* **目标随机化** ：接触广告的用户
* **样本量计算** ：为确保实验的统计功效和显著性，计算出每组所需样本量为251，总样本量为502。
* **实验运行时间** ：从2020年7月3日到2020年7月10日。

### 随机抽样

* 数据中删除了没有实验结果的记录。
* 对于实验组（互动广告）和对照组（静态广告），分别随机抽取了251个样本。

### 数据分析

1. **数据可信度** ：

* 数据按日期排序，确保实验时间内的数据完整性。
* 对数据进行清洗，确保分析数据的准确性。

1. **样本分配检验** ：

* 使用卡方检验（Chi-square Test）对样本分配进行检验，结果显示没有显著的样本不一致（SRM）。

1. **转化率计算** ：

* 控制组转化率：0.49
* 实验组转化率：0.45

1. **假设检验** ：

* 使用z检验计算得出z统计量为-1.073，p值为0.858，远大于显著性水平α = 0.05。
* z统计量未超过z临界值，未能拒绝原假设，即互动广告的转化率未显著优于静态广告。

1. **置信区间** ：

* 95%置信区间为[-0.134, 0.039]，表明引入互动广告可能导致转化率下降最多13.3%或增加最多3.9%。

### 结论

根据实验数据，互动广告并未显著提高转化率。尽管存在一定的波动，但由于p值较高且置信区间包含零，我们无法拒绝原假设，即互动广告的转化率未显著优于静态广告。