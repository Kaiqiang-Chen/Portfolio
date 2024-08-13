# Portfolio - Kaiqiang Chen

This Portfolio is a compilation of all the projects I have done for academic, self-learning and hobby purposes, covering various fields incl. **Data Science & Data Analysis**, **Product Management** and **Coonsulting**. This portfolio also contains my Achievements, skills, and certificates. It is updated on the regular basis.

- **Email**: [kaiqiang.chen@outlook.com](kaiqiang.chen@outlook.com)
- **LinkedIn**: [www.linkedin.com/in/kenneth-kaiqiang-chen](https://www.linkedin.com/in/kenneth-kaiqiang-chen)

## I. Awards

- Recipient of **2nd Prize**, *Scholarahip & Merit Student* of Wuhan University
- **Meritorious Winner**, *2024 Interdisciplinary Contest In Modeling (ICM)* (Top 7%)
- Recipient of **National 2nd Prize**, *Citi Cup Financial Innovation Application Contest* (Top 15 among 152 teams)
- Recipient of **National 1st Prize**, *2022 National College Business Elite Challenge (CUBEC) International Trade Competition*
- Recipient of **National 1st Prize**, *2022 National English Competition for College Students (NECCS)* (Top 5‰)

## II. Data Science & Data Analysis Projects

### 1. Data Manipulation and EDA

**[Superstore Sales Performance Dashboard](https://public.tableau.com/views/SalesPerformanceDashboard_17224722585070/sheet0?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link "Lick to open the dashboard website")**

<br />

### 2. Dashboard Building with Tableau

`![test]("https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/Superstore.jpg")` **[Superstore Sales Performance Dashboard](https://public.tableau.com/views/SalesPerformanceDashboard_17224722585070/sheet0?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link "Lick to open the dashboard website")**

In this project I have used survival analysis to study how the likelihood of the customer churn changes over time. I have also implementd a Random Forest model to predict the customer churn and deployed a model using flask webapp on Heroku. [App](https://churn-prediction-app.herokuapp.com/)
Segmentation and affinity analysis are also done to study user purchase patterns.

<br />

### 3. Machine Learning

`![test2]("https://raw.githubusercontent.com/Kaiqiang-Chen/images/main/1723448665294.jpg") ` **[Kaggle | House Prices - Advanced Regression Techniques](https://github.com/Kaiqiang-Chen/Portfolio/blob/878769faa1fef4dae7661c2e0ee516bfa9f0ebd7/Data%20Science%20%26%20Data%20Analysis/Dashboard%20Building%20with%20Tableau/Readme_Dashboard.md)**

【概述】利用房屋面积、房间数量、车库容量等共81个变量，1400+训练集样本对Ames, Iowa的房屋价格进行预测，包括缺失值处理、特征工程、机器学习及集成。

* **特征工程：** 对缺失值和异常值进行处理；调整目标变量偏态分布；利用seaborn绘制热力图，挖掘变量相关性以及与目标函数高度相关的特征；利用LabelEncoder和one-hot编码将部分类别型特征转化为数值型特征；利用Box-Cox处理高偏态数值型特征。
* **机器学习：** 调用XGboost、KNN、SVM等8种模型预测并进行Bagging、Stacking集成，最终RMSE 0.1183，排名 **Top 2%** 。

<br />

### 4. Causal Inference and A/B Test

`<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812164954.png">` **[Interactive Ads and User Conversion Rates: An A/B Test](https://github.com/archd3sai/News-Articles-Recommendation)**

A hybrid-filtering personalized news articles recommendation system which can suggest articles from popular news service providers based on reading history of twitter users who share similar interests (Collaborative filtering) and content similarity of the article and user’s tweets (Content-based filtering).

<br />

### 5. Data Modeling

``<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812164338.png">```  **[Weather the Storm: Mastering Insurance &amp; Site Selection](https://github.com/archd3sai/News-Articles-Recommendation)**

【概述】全球各地极端气候不断增多，保险公司对极端气候地区房产承保风险变大，面临是否要减少承保的决策。我们通过ARIMA预测极端天气，利用EWM-TOPSIS评估保险风险，并提出地标保护建议，帮助保险公司决策及业主评估选址，优化风险管理与决策。

* 运用ARIMA模型预测极端天气发生概率，构建EWM-TOPSIS和AHP-FCE模型进行保险承保风险评估，有效降低承保风险。
* 通过Python或R实施ARIMA时间序列分析，并使用多种图表可视化展示极端天气预测结果及风险评估成果，提升决策透明度。
* 运用风险评估及项目成本收益分析，支持保险承保决策，助力优化资源配置并提高投资回报率。

<br />

### 6. Other Capstone Projects

`<img align="left" width="250" height="150" src="https://github.com/archd3sai/Portfolio/blob/master/Images/airplane.jpeg">` **[Predictive Maintenance of Aircraft Engine](https://github.com/archd3sai/Predictive-Maintenance-of-Aircraft-Engine)**

In this project I have used models such as RNN, LSTM, 1D-CNN to predict the engine failure 50 cycles ahead of its time, and calculated feature importance from them using sensitivity analysis and shap values. Exponential degradation and similarity-based models are also used to calculate its remaining life.

<br />

## III. Product Management

`<img align="left" width="250" height="150" src="https://github.com/archd3sai/Portfolio/blob/master/Images/960x0.jpg">` **[PropriskAI - One-Stop Real Estate Risk Informa Service](https://github.com/archd3sai/Wind-Turbine-Power-Curve-Estimation)**

【概述】近期某些房地产公司发生债券违约事件，爆发了流动性危机，上游供应商的应收账款也会面临账期延长，乃至形成坏账的可能，但是这些风险信息比较分散。我们利用AI挖掘以及学习技术，解决信息分散、非结构化的问题，自助构建数据集并提出客观评估房地产企业流动性危机影响范围和规模的模型和方法，为广大房地产下游供应商和投资者的决策提供了风险评估参考。

* [**产品策划：**]()针对房地产风险信息分散影响广大投资者和下游供应商决策的痛点，带领10余名成员1个月内从0到1搭建房地产流动性风险评估平台，并通过种子用户验证PMF，获得证券研究所所长、房产供应商和金融科技企业CEO等众多专家的认可。
* **数据挖掘：** 通过随机森林、XGBoost和神经网络等机器学习算法（结合文献研究）进行建模，确定房地产风险预测、供应商风险评估、财务指标预测等5大模型；利用GenAI进行数据挖掘，将自动化爬虫脚本采集的非结构化信息结构化，解决技术难点。

<br />

## IV. Consulting Reports

### 1. Five-Year Growth Strategy for Banbao (2023 Oliver Wyman Impact Case Competition | Team OWesome)

`<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812165158.png">` **[Five-Year Growth Strategy for Banbao](https://github.com/archd3sai/Predicting-GDP-of-India)**

【概述】赛题要求为中国积木玩具行业的领先企业制定增长战略。该企业在拥有20年运营经验的基础上，面临来自全球巨头和本地新兴竞争者的激烈竞争，计划在五年内将收入翻倍。赛题涉及市场动态分析、竞争格局研究、品类多元化、渠道更新以及品牌定位策略的制定，旨在帮助企业抓住新兴品类与电商渠道的增长机会。

* **项目统筹：** 选择国内某积木玩具龙头企业作为客户设计收入增长战略，3 周内完成 30 页 Deck，负责统筹整体故事线的搭建。
* **市场研究：** 对积木玩具行业和龙头进行全方位的研究和对标分析，得出行业规模增速及驱动力、竞争格局、KSFs 和发展趋势。
* **客群划分：** 通过问卷调查 (N=389) 获得一手消费者数据，提炼不同人群消费者画像和KPCs，聚类目前主要客群和潜在目标客群。
* **战略设计：** 对标头部品牌制定全渠道战略和门店选址方案；结合案例研究设计新产品和爆款营销策略；设计新渠道推广策略。

<br />

### 2. Carbon neutralization strategy for TNC in Dairy Industry (2023 Bain Case Competition | Team XiaoBaoBain)

`<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812165054.png">` **[Carbon neutralization strategy for TNC in Dairy Industry](https://github.com/archd3sai/Predicting-GDP-of-India)**

In this project I applied various classification models such as Logistic Regression, Random Forest and LightGBM to detect consumers who will default the loan. SMOTE is used to combat class imbalance and LightGBM is implemented that resulted into the highest accuracy 98.89% and 0.99 F1 Score.

<br />

## V. Exploration in Other Fields

- ### Metaheuristic Algorithms

  - [Genetic Algorithm](https://github.com/archd3sai/Statistical-Methods/blob/master/genetic-algorithm.ipynb) : In this file, I have implemented simple genetic algorithm that finds out the list of numbers which equal to any specified number when summed together.
- ### Operations Research

  - [SQL Challenges](https://github.com/archd3sai/SQL): This repository contains codes of online SQL challenges (From Hackerrank, Leetcode, Testdome, etc.) solved by me.
  - [Data Science Challenges](https://github.com/archd3sai/DS-Challenges): This repository contains codes of online Data Science challenges (From Hackerrank, TestDome, etc.) solved by me.
- ### Bayesian Statistic

  - [Ranking of NFL teams using Markov-chain methods](https://github.com/archd3sai/Ranking-of-NFL-Teams-using-Markov-method/blob/master/Ranking%20of%20NFL%20teams%20Report.pdf) : In this project I implemented and compared three stationary distribution of Markov-chain based approaches to rank 32 NFL (National Football League) teams from "Best" to "Worst" using the scores of 2007 NFL regular season.
  - [Ranking of Tennis players](https://github.com/archd3sai/Tennis-Players-Ranking/blob/master/TennisRanking.ipynb) : Objective of this project is to rank all Tennis Players based on the matches they played in the year of 2018. This project comprises 4 approaches to rank Tennis players and I have tried to make these approaches more robust sequentially.

## VI. Core Competencies

- **Methodologies**: Machine Learning, Statistics, Big Data Analytics, Causal Inference(Econometrics), Bayesian Statistics (MCMC), Data Structure and Algorithm, Operation Research
- **Languages**: Python (Proficient, EDA[Numpy, Pandas, Matplotlib, Seaborn] / ML[sklearn] / Scrawling [request, re, selenium, xpath] / Optimization [Gurobipy]), SQL(Proficient[partition, ETL]), R(Proficient[Dplyr, Tidyr, ggplot2,mlr3]), Java, C++
- **Tools**: MySQL, Tableau, PowerBI, Quicksight, Git, Amazon Web Services (AWS), MS Office (Thinkcell)
