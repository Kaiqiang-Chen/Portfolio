# 作品集 - 陈凯强 Portfolio

这份作品集汇集了我在实践、学术和自由探索完成的一些项目，涵盖了**数据科学与数据分析**、**产品设计**和**咨询**等多个领域。也涵盖我的成就、技能等。将不定期更新。

This Portfolio is a compilation of all the projects I have done for academic, self-learning and hobby purposes, covering various fields incl. **Data Science & Data Analysis**, **Product Management** and **Consulting**. This portfolio also contains my Achievements, skills, and certificates. It is updated on the regular basis.

**联系方式 [CONTACTS]**

- **Email**: [kaiqiang.chen@outlook.com](kaiqiang.chen@outlook.com)
- **LinkedIn**: [www.linkedin.com/in/kenneth-kaiqiang-chen](https://www.linkedin.com/in/kenneth-kaiqiang-chen)

## I. 曾获荣誉 Awards

校乙等奖学金、美赛M奖、花旗杯国家级二等奖、商业精英挑战赛国家级一等奖、大英赛国家级一等奖、互联网+省银奖等

- Recipient of **2nd Prize** *Scholarship & Merit Student* of Wuhan University
- **Meritorious Winner**, *2024 Interdisciplinary Contest In Modeling (ICM)* (Top 7%)
- Recipient of **National 2nd Prize**, *Citi Cup Financial Innovation Application Contest* (Top 5 among 152 teams)
- Recipient of **National 1st Prize**, *2022 National College Business Elite Challenge (CUBEC) International Trade Competition*
- Recipient of **National 1st Prize**, *2022 National English Competition for College Students (NECCS)* (Top 5‰)

## II. 数据科学 & 数据分析项目 Data Science & Data Analysis Projects

### 1. 数据清洗、探索与可视化 Data Manipulation and EDA

<img align="left" width="250" height="150" src="https://raw.githubusercontent.com/Kaiqiang-Chen/images/main/portfolio/20240814133515.png"> **[中国上市公司的分布与疫情下发展状况的探究 [12/2023] [R, Python]](https://github.com/Kaiqiang-Chen/Portfolio/tree/6bf1ae485af8bb6748b903f69a48cb696547488c/01_Data%20Science%20%26%20Data%20Analysis/1.%20Data%20Manipulation%20%26%20EDA/Stock%20Data%20Visualization%20and%20Exploration)**

出于对疫情背景下不同企业发展情况的好奇，从上市公司数据着手，利用Tushare API接口获取财务数据，通过柱状图、玫瑰图、散点图、箱线图等多种类型图表探究上市公司分布特征以及疫情对不同行业的影响，通过PCA、SOM、K-Means等非监督机器学习方法进行降维与聚类。

<br />

### 2. 制作数据看板 (Tableau) Dashboard Building with Tableau

<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/Superstore.jpg"> **[美国商超业绩数据看板 [08/2024] [Tableau]](https://public.tableau.com/views/SalesPerformanceDashboard_17224722585070/sheet0?:language=zh-CN&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link "Lick to open the dashboard website")**

利用美国商超零售数据制作可视化、可交互数据看板，呈现不同年份分地区、分州（包括每个州Top5城市）、分品类、分子品类以及渠道的销售数据和趋势，轻松并可通过点击不同组件实现全局筛选器，能够轻松监控业绩表现并归因。

<br />

### 3. 机器学习 Machine Learning

<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812164456.png"> **[Kaggle | House Prices - Advanced Regression Techniques [05/2024] [Python]](https://github.com/Kaiqiang-Chen/Portfolio/tree/2adf7d4a0cdb6707b5b3972c952422266ff42150/01_Data%20Science%20%26%20Data%20Analysis/2.%20Machine%20Learning/Supervised%20ML%20-%20House%20Pricing)**

利用Kaggle数据集，通过81个变量、1400+样本对爱荷华州的房屋价格进行预测。首先进行特征工程，对缺失值异常值进行处理；利用seaborn绘制热力图，洞察变量相关性，挖掘与目标函数高度相关的特征；利用LabelEncoder和one-hot编码将部分类别型特征转化为数值型特征等。然后调用XGboost、KNN、SVM等8种ML模型预测并进行Stacking集成，最终排名可进入Top 2%。
<br />

### 4. 因果推断与A/B实验 Causal Inference and A/B Test

<img align="left" width="250" height="150" src="https://raw.githubusercontent.com/Kaiqiang-Chen/images/main/20240814194313.png"> **[PSM-DID 政策效应研究论文复刻 [05/2024] [Stata]](https://github.com/Kaiqiang-Chen/Portfolio/tree/2adf7d4a0cdb6707b5b3972c952422266ff42150/01_Data%20Science%20%26%20Data%20Analysis/6.%20Other%20Capstones/PSM-DID%E6%94%BF%E7%AD%96%E6%95%88%E5%BA%94%E7%A0%94%E7%A9%B6%E8%AE%BA%E6%96%87%E5%A4%8D%E5%88%BB)**

复刻了一篇关于全球变暖背景下中国碳市场碳减排效应的研究，基于市场机制与行政干预的协同作用视角，利用PSM-DID方法，检验了试点地区碳市场促进碳减排的理论机理与政策效果，包括平行趋势检验、安慰剂检验、PSM半径匹配/近邻匹配/核匹配/剔除其他政策以及特殊样本影响的稳健性分析，以及碳价、市场流动性和相对市场交易规模三个机制变量的传导机制分析。

<br />

<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812164954.png"> **[A/B实验：互动广告是否能提高用户转化率？ [06/2024] [Python]](https://github.com/Kaiqiang-Chen/Portfolio/tree/2adf7d4a0cdb6707b5b3972c952422266ff42150/01_Data%20Science%20%26%20Data%20Analysis/4.%20Causal%20Inference%20%26%20AB%20Testing/AB%20Test%20-%20Advertising/Interactive%20Ads%20and%20User%20Conversion%20Rates%20-%20%20An%20AB%20Test)**

设计并实施互动广告与静态广告对比的A/B测试，目标为提升用户转化率。通过精确计算样本量和严格的假设检验，确保了实验的科学性。实验结果显示互动广告的转化率与静态广告无显著差异，未能拒绝原假设，能够帮助公司有效避免不必要的广告投入。

<br />

### 5. 数据建模 Data Modeling

<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812164338.png">  **[Weather the Storm: Mastering Insurance &amp; Site Selection [01/2024] [Python]](https://github.com/Kaiqiang-Chen/Portfolio/tree/16e16a977d3af3dd40fb87d85d986752f8e718a8/01_Data%20Science%20%26%20Data%20Analysis/5.%20Data%20Modeling)**

全球各地极端气候不断增多，保险公司对极端气候地区房产承保风险变大，面临是否要减少承保的决策。我们通过ARIMA预测极端天气，利用EWM-TOPSIS评估保险风险，并提出地标保护建议，帮助保险公司决策及业主评估选址，优化风险管理与决策。报告最终获得**美赛M奖**，排名前Top 7%。

<br />

### 6. 其他实践项目 Other Capstone Projects

<img align="left" width="250" height="150" src="https://raw.githubusercontent.com/Kaiqiang-Chen/images/main/portfolio/20240814132016.png"> **[关于多旅行商问题(MTSP)的启发式算法研究（小组完成） [04/2024] [Python]](https://github.com/Kaiqiang-Chen/Portfolio/tree/2adf7d4a0cdb6707b5b3972c952422266ff42150/01_Data%20Science%20%26%20Data%20Analysis/6.%20Other%20Capstones/%E5%85%B3%E4%BA%8E%E5%A4%9A%E6%97%85%E8%A1%8C%E4%B8%8A%E9%97%AE%E9%A2%98(MTSP)%E7%9A%84%E5%90%AF%E5%8F%91%E5%BC%8F%E7%AE%97%E6%B3%95%E7%A0%94%E7%A9%B6%EF%BC%88%E5%B0%8F%E7%BB%84%EF%BC%89)**

旅行商问题是运筹学中的经典问题。我们拓展了经典问题的情境假设使其更贴合实际问题，并以多仓库、封闭情形为例展开启发式算法研究。我们分大规模问题和小规模问题两种情形，首先用Python中的Gurobipy库实现线性规划的求解，然后通过Genetic Algorithm(GA)、Simulated Annealing(SA) 等启发式算法求解并进行优化，比较不同求解方法优劣（求解结果和效率）。

<br />

## III. 产品设计 Product Management

<img align="left" width="250" height="150" src="https://raw.githubusercontent.com/Kaiqiang-Chen/images/main/portfolio/20240814134150.png"> **[PropriskAI-一站式房地产风险信息全视域 AI [01/2024-05/2024] [Python, Figma, Draw.io]](https://github.com/Kaiqiang-Chen/Portfolio/tree/2adf7d4a0cdb6707b5b3972c952422266ff42150/02_Product%20Management/PropriskAI%E2%80%94%E2%80%94%E4%B8%80%E7%AB%99%E5%BC%8F%E6%88%BF%E5%9C%B0%E4%BA%A7%E9%A3%8E%E9%99%A9%E4%BF%A1%E6%81%AF%E6%9C%8D%E5%8A%A1%E5%85%A8%E8%A7%86%E7%95%8CAI)**

某些房地产公司爆发流动性危机，上游供应商的应收账款面临账期延长，但这些风险信息可能分散在研报、投资者问答等各处，供应商和投资者难以及时获知并准确评估风险和决策。我们利用AI数据挖掘和机器学习算法，自主构建数据集和模型完成这款AI产品，解决风险范围难界定、程度难量化等痛点，荣获**花旗杯全国二等奖**。

<br />

## IV. 咨询报告 Consulting Reports

### 1. 贝恩实习期间参与零售行业报告

<img align="left" width="250" height="150" src="https://raw.githubusercontent.com/Kaiqiang-Chen/images/main/portfolio/20240814133802.png"> **[贝恩联合中国连锁经营协会：2023中国生鲜快消品零售业态发展趋势研究报告 [07/2023 - 10/2023]](https://www.bain.cn/news_info.php?id=1751)**

共参与制作 ~10 页报告：研究国内 8 大零售业态现状，并参考西方硬折扣店发展历程判断未来趋势；提出商超门店集中度与利润率正相关的假设，通过年报等搜集数据，并进行回归分析验证假设，建议零售商在核心区域高密度布局发挥规模优势等。

<br />

### 2. 明天美好咨询服务公司 (ABC美好社会咨询社) 某国际高校数字化咨询项目

<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240814192324.png"> **[报告因客户隐私不便公开 [01/2024 - 06/2024]](https://www.theabconline.org/)**

担任正式数字化咨询师，为国际高校人事部推进数字化，通过访谈调研梳理场景、痛点，针对人事部难以客观量化评估薪酬绩效的痛点，设计广义模糊决策树 (FPT) 机器学习解决方案来客观确定计算模型，并分析输出指标业务价值，获得校长高度认可。项目组被评为ABC优秀项目组，个人获得优秀PC荣誉。


<br />

### 3. 2023 “奥玮杯”咨询案例大赛报告（队长）

<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812165158.png"> **[Five-Year Growth Strategy for Banbao | Team OWesome [04/2023]](https://github.com/Kaiqiang-Chen/Portfolio/blob/2adf7d4a0cdb6707b5b3972c952422266ff42150/03_Consulting%20Reports/5-Year%20Strategy%20for%20Banbao_Team%20OWesome%20Final_Captain_Kaiqiang%20Chen.pdf)**

中国积木玩具行业的领先企业正面临来自全球巨头和本地新兴玩家的激烈竞争。我们为客户制定收入增长战略。通过行业研究得出行业规模增速及驱动力、竞争格局、KSF和发展趋势；通过问卷调查获得一手消费者数据，聚类不同客群，提炼消费人群画像和KPC；最终设计战略，对标头部品牌制定全渠道战略和门店选址方案，并结合案例研究设计新产品和爆款营销策略等。
<br />

### 4. 2023 “贝恩杯”咨询案例大赛报告 
<img align="left" width="250" height="150" src="https://ck-obsidian.oss-cn-hangzhou.aliyuncs.com/20240812165054.png"> **[Carbon neutralization strategy for TNC in Dairy Industry | Team XiaoBaoBain [05/2023]](https://github.com/Kaiqiang-Chen/Portfolio/blob/2adf7d4a0cdb6707b5b3972c952422266ff42150/03_Consulting%20Reports/Carbon%20neutralization%20strategy%20for%20TNC%20Industry_Team%20XiaoBaoBain.pdf)**

当前畜牧业正面临甲烷排放等碳中和挑战。环保非营利组织(NGO)首席战略官提出，希望通过试点推进可持续畜牧业实践，借鉴发达国家减排措施，并探讨NGO在其中的作用。我们回答了关于选择关注的畜牧业子行业、碳中和痛点、优先试点的农场类型及关键减排措施等核心问题，向TNC(NGO) 提供战略建议。

<br />


## V. 核心技能 Core Competencies

-	**代码能力**：**Python** (熟练，EDA[Numpy, Pandas, Matplotlib] / 机器学习[sklearn] / 爬虫[request, re, selenium] / 规划求解[Gurobipy]), **SQL** (熟练，窗口函数，数仓ETL), **R** (熟练，Dplyr, Tidyr, ggplot2,mlr3), Java, C++, Git
-	**数理能力**：数据结构、元启发式算法、贝叶斯统计 (MCMC)、运筹学、离散数学、机器学习、概率统计 (SPSS)、因果推断/计量 (Stata) 
-	**其他技能**：英语 (GRE: 325/340 + W4); Tableau/Tableau; AWS; AARRR/RFM/漏斗等业务分析模型；MS Office (Thinkcell); Figma, Canvas, Draw.io

<br />

- **Methodologies**: Machine Learning, Statistics, Big Data Analytics, Causal Inference (Econometrics), Bayesian Statistics (MCMC), Data Structure and Algorithm, Operation Research
- **Languages**: **Python** *(Proficient, EDA[Numpy, Pandas, Matplotlib] / ML[sklearn] / Scrawling [request, re, selenium, xpath] / Optimization [Gurobipy])*, **SQL** *(Proficient[partition, ETL])*, **R** *(Proficient[Dplyr, Tidyr, ggplot2,mlr3])*, Java, C++
- **Tools**: MySQL, Tableau, PowerBI, Quicksight, Git, Amazon Web Services (AWS), SPSS, MS Office (Thinkcell), Figma, Canvas, Draw.io
- **Others**: English (GRE: 325/340 + W4)
