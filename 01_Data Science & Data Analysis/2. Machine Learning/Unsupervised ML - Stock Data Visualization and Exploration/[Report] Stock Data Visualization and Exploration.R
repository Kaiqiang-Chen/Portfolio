pacman::p_load(dplyr,openxlsx,tidyverse, mclust, psych, GGally, factoextra,patchwork,ggrepel,ggfortify,ggthemes,showtext)

theme_set(theme_bw())

data <- read.xlsx("C:/Users/10136/PycharmProjects/pythonProject/filtered_stock_info.xlsx")

data %>% group_by(industry) %>% summarize(n=n()) %>% arrange(desc(n)) %>% head(10)
#前十个行业及上市公司个数


data %>%
  group_by(industry) %>%
  summarize(n=n()) %>%
  mutate(pct = n / sum(n)) %>%
  ggplot(aes(x = reorder(industry, n), y = n,fill = n)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = n, y = n-10),color="white") +
  geom_text(aes(label = paste0(round(100 * pct, 1), "%"), y = n + 15)) +
  scale_fill_gradient(low ="#FFC2C2", high = "#990000") +
  coord_flip() +
  theme_minimal()
  xlab("行业") + ylab("数量") +
  ggtitle("上市公司行业数量分布图（截至2018）") +
  theme(plot.title = element_text(hjust = 0.5))

##玫瑰图
  
data %>%
  group_by(industry) %>%
  summarize(n=n()) %>%
  mutate(pct = n / sum(n)) %>%
  ggplot(aes(x = reorder(industry, n), y = n,fill = n)) +
  scale_fill_gradient(low ="#FFC2C2", high = "#990000") +
  geom_bar(stat = "identity") +
  geom_text(aes(label = n, y = n-10),color="white") +
  coord_polar()+
  theme_minimal()+
  xlab("行业") + ylab("数量") +
  ggtitle("上市公司行业数量分布图（截至2018）") +
  theme(plot.title = element_text(hjust = 0.5))


#雇员数总体分布
data %>%
  group_by(industry) %>%
  summarize(n=sum(`employee#`)) %>% 
  ggplot(aes(x = reorder(industry, n), y = n,fill = n)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = n, y = n-65000),color="white") +
  scale_fill_gradient(low ="#FFC2C2", high = "#990000") +
  coord_flip() +
  theme_minimal()+
  xlab("行业") + ylab("雇员数量") +
  ggtitle("上市公司分行业雇员分布图（截至2018）") +
  theme(plot.title = element_text(hjust = 0.5))


summary(data$'employee#')
ggplot(data, aes(x = factor(industry), y = `employee#`)) +  # 箱线http://127.0.0.1:25711/graphics/plot_zoom_png?width=1301&height=914图函数  
  geom_boxplot()+
  coord_flip()

#雇员数
data %>%
  group_by(industry) %>%
  summarize(n=sum(`employee#`)) %>% 
  arrange(desc(n)) %>% 
  head(10)


xlab("行业") + ylab("数量") +
  ggtitle("上市公司行业数量分布图（截至2018）") +
  theme(plot.title = element_text(hjust = 0.5))

ggplot(data, aes(x = factor(industry), y = `income_2019`)) +  # 箱线图函数  
  geom_boxplot()+
  coord_flip()

ggplot(data, aes(x = factor(industry), y = `income_2019`)) +  # 箱线图函数  
  geom_boxplot(outlier.shape = NA)+
  coord_flip()+
  scale_y_continuous(limits = quantile(data$`income_2019`, c(0.1, 0.9)))

summary(data$`incomeYOY%_even`)

ggplot(data,aes(y=`incomeYOY%_even`))+
  geom_boxplot()
#必须去掉异常值

# 计算箱线图统计量
stats <- boxplot.stats(data$'incomeYOY%_even')$stats
stats
df <- data.frame(x="", ymin=stats[1], lower=stats[2], middle=stats[3],
                 upper=stats[4], ymax=stats[5])

# 画出箱线图
p <- ggplot(df, aes(x=x, lower=lower, upper=upper, middle=middle, ymin=ymin,
                    ymax=ymax)) +
  geom_boxplot(stat="identity")+
  labs(title="2019-2022平均营收增长率",x="incomeYOY%_even")+
  theme_classic()+
  theme(plot.title=element_text(hjust=0.5))
p

## ---- 结论：营收基本上还是增长的

summary(data$`profitYOY%_even`)

stats1 <- boxplot.stats(data$`profitYOY%_even`)$stats
stats1
df1 <- data.frame(x="", ymin=stats1[1], lower=stats1[2], middle=stats1[3],
                 upper=stats1[4], ymax=stats1[5])

# Create plot
p1 <- ggplot(df1, aes(x=x, lower=lower, upper=upper, middle=middle, ymin=ymin,
                    ymax=ymax)) +
  geom_boxplot(stat="identity")+
  labs(title="2019-2022平均净利润增长率",x="profitYOY%_even")+
  theme_classic()+
  theme(plot.title=element_text(hjust=0.5))
p1
## ----结论：净利润情况比收入要差，基本没有增长，亏损的企业更多


datatb <- as_tibble(data) %>% mutate(area_hubei=ifelse(area=="湖北",1,0))
datatb

#不同行业的表现
datatb  %>% group_by(`11index`) %>% summarize(median(`incomeYOY%_even`))
datatb  %>% group_by(`11index`) %>% summarize(median(`incomeYOY%_var`)) 

datatb  %>% filter(`11index`==4) %>% summarize(median(`incomeYOY%_2019`))
datatb  %>% filter(`11index`==4) %>% summarize(median(`incomeYOY%_2020`))
datatb  %>% filter(`11index`==4) %>% summarize(median(`incomeYOY%_2021`))
datatb  %>% filter(`11index`==4) %>% summarize(median(`incomeYOY%_2022`))


datatb <- datatb %>% group_by(area_hubei)
datatb  %>% summarize(mean(`incomeYOY%_2020`))

#`mean(\`incomeYOY%_2020\`)`异常高，找原因
summary(datatb$'incomeYOY%_2020')
#Max值竟然达到16849.847，说明异常值存在可能极大地影响了平均值

#说明湖北上市公司在2020年营收也难免受疫情影响
i2019 <- datatb  %>% summarize(median(`incomeYOY%_2019`))
i2020 <- datatb  %>% summarize(median(`incomeYOY%_2020`))
i2021 <- datatb  %>% summarize(median(`incomeYOY%_2021`))
i2022 <-datatb %>% summarize(median(`incomeYOY%_2022`))
income_change <- i2019 %>% left_join(i2020) %>% left_join(i2021) %>% left_join(i2022)
view(income_change)
p2019 <- datatb  %>% summarize(median(`profitYOY%_2019`))
p2020 <- datatb  %>% summarize(median(`profitYOY%_2020`))
p2021 <- datatb  %>% summarize(median(`profitYOY%_2021`))
p2022 <-datatb  %>% summarize(median(`profitYOY%_2022`))
profit_change <- p2019 %>% left_join(p2020)%>% left_join(p2021) %>% left_join(p2022)
view(profit_change) 



# 接下来探究在疫情期间增长比较好的企业的特征
# 剔除了营收或净利润平均yoy绝对值>1k的异常值



#PCA
# 比较平稳的企业的特征
datatb <- datatb %>% filter(`incomeYOY%_even`<200,`profitYOY%_even`<200,`incomeYOY%_even`>-200,`profitYOY%_even`>-200)
datatb %>% select(-`incomeYOY%_even`)
pca1 <- datatb %>% dplyr::select(-`incomeYOY%_even`,-`incomeYOY%_var`,-`3index`,-industry,-`industry_index`,-`profitYOY%_2019`,-`11index`,-`incomeYOY%_2019`,-area_hubei,-name,-area,-ts_code,-list_date,-symbol,-'incomeYOY%_2020',-'incomeYOY%_2021',-'incomeYOY%_2022',-'profitYOY%_2020',-'profitYOY%_2021',-'profitYOY%_2022',-'profitYOY%_even',-'profitYOY%_var')
view(pca1) #注意这里不加dyplr的话会跟别的包里的select混起来，所以报错
datatb<-as.matrix(scale(datatb))
pca_data <- datatb %>% dplyr::select(-status,-`incomeYOY%_even`,-`incomeYOY%_var`,-`3index`,-industry,-`industry_index`,-`profitYOY%_2019`,-`11index`,-`incomeYOY%_2019`,-area_hubei,-name,-area,-ts_code,-list_date,-symbol,-'incomeYOY%_2020',-'incomeYOY%_2021',-'incomeYOY%_2022',-'profitYOY%_2020',-'profitYOY%_2021',-'profitYOY%_2022',-'profitYOY%_even',-'profitYOY%_var')
pca_data<-as.matrix(scale(pca_data))

pca <- pca_data %>% 
  prcomp(center = T, scale = T) #作用相当于转置。center平移，scale拉伸
pca
summary(pca) #proportion of variance 方差占样本总方差的比例


pcaDat <- get_pca(pca)
fviz_pca_ind(pca, label = "none", habillage = datatb$'status', addEllipses = T, ellipse.level = 0.9) +
  scale_color_brewer(palette = "Set1")

fviz_pca_biplot(pca, label = "var")
fviz_pca_var(pca)
fviz_screeplot(pca, addlabels = T, choice = "eigenvalue") #特征值
fviz_screeplot(pca, addlabels = T, choice = "variance") #方差

##ggplot
stockPCA <- datatb %>% 
  mutate(PCA1 = pca$x[,1], PCA2 = pca$x[,2],PCA3 = pca$x[,3])
ggplot(stockPCA, aes(PCA1, PCA2, col = transIndex)) +
  geom_point() +
  stat_ellipse(level = 0.9)
ggplot(stockPCA, aes(PCA1, PCA3, col = transIndex)) +
  geom_point() +
  stat_ellipse(level = 0.9)

#kmeans
pacman::p_load(mlr3,mlr3verse,mlr3cluster,mlr3viz,GGally,mlr3tuning,mlr3learners)

gvhdCtrlScale <- as.data.table(scale(pca1))#标准化操作将数据转换为均值为0、标准差为1的形式，有助于消除不同变量之间的量纲差异。
ggscatmat(gvhdCtrlScale)#使用GGally包中的ggscatmat函数绘制了标准化后的散点矩阵图。
ggpairs(gvhdCtrlScale,
        upper = list(continuous = "density"),
        lower = list(continuous = wrap("points", size = 0.4)),
        diag = list(continuous = "densityDiag"))
#使用GGally包中的ggpairs函数绘制了成对图，更详细地显示了变量之间的关系。
#具体地，上半部分是核密度图，对角线上是每个变量的密度图，下半部分是散点图。
#这有助于更深入地了解变量之间的相关性和分布

#选择task和learner 设置参数

gvhdCtrlScale <- gvhdCtrlScale %>% rename(employee_num=`employee#`)
gvhdCtrlScale <- gvhdCtrlScale %>% rename(netPorfitRate2019=`netprofit%_2019`)
taskC = TaskClust$new("gvhdCtrlScale", gvhdCtrlScale) #如果是监督学习还要加上目标，非监督就没有
class(taskC)
autoplot(taskC)
taskPos = TaskClust$new("gvhdCtrlPos", as.data.table(scale(GvHD.pos)))

mlr_learners$keys("clust")
kmeans_lrn = lrn("clust.kmeans")
class(kmeans_lrn)
kmeans_lrn$param_set$params #超参数集合
kmeans_lrn$param_set$values = list(centers = 3, iter.max = 100, nstart = 10)

#训练模型及预测
kmeans_model <- kmeans_lrn$train(taskC)
print(kmeans_model$model)
kmeans_lrn$stategvhdCtrlScale
kmeans_lrn$assignments

kmeans_lrn1 = kmeans_lrn$clone()
kmeans_lrn1$predict(taskC)
autoplot(kmeans_lrn1$predict(taskC),taskC, type = "scatter" )

kmeansPos = kmeans_lrn$predict(taskPos)

autoplot(kmeansPos, taskPos, type = "pca", frame = T) # 还有type="sil"是剪影图
autoplot(kmeansPos, taskPos, type = "sil", frame = T) 


#som
pacman::p_load(tidyverse, mclust, Rtsne,umap,kohonen, lle, GGally, plot3D, plot3Drgl)
theme_set(theme_bw())


somGrid <- somgrid(xdim = 5, ydim = 5, topo = "hexagonal",
                   neighbourhood.fct = "bubble", toroidal = F)
#表示按六边形将神经网络单元排成5列、5行，共计25个单元。

#设定 topo=rectangular,toroidal=T， 重新运行 SOM 比较。
flea2 <- pca1%>% 
  scale()

fleaSom <- som(flea2, grid = somGrid, rlen = 50000, alpha = c(0.05, 0.01))
fleaSom1 <- som(flea2, grid = somGrid, rlen = 100000, alpha = c(0.1, 0.001))
#rlen 迭代次数，alpha学习率
par(mfrow = c(2,3))
plotType <- c("codes", "changes", "counts", "quality", "dist.neighbours", "mapping")
walk(plotType, ~plot(fleaSom, type = ., shape = "straight"))

walk(plotType, ~plot(fleaSom1, type = ., shape = "straight"))

# 可以让这些图分别显示
## plot(fleaSom,type="codes") 里面半径大小说明权重大小，但是并不知道是半径越大还是越小
## plot(fleaSom,type="changes")
## trainning表示训练过程 看迭代后是否达到稳定
## count和mapping其实表达的是一个意思 都是看数量
## quality看点和碗有多匹配
# neighbor 领域距离图 计算每个碗中的点和周围的碗中的点的距离的平均值 越红距离越小
getCodes(fleaSom) %>% 
  as_tibble() %>% 
  iwalk(~plot(fleaSom, type = "property", property = .,
              main = .y, shape = "straight"))

getCodes(fleaSom1) %>% 
  as_tibble() %>% 
  iwalk(~plot(fleaSom1, type = "property", property = .,
              main = .y, shape = "straight"))

#SNE
pacman::p_load(tidyverse, mclust, Rtsne,umap,kohonen, lle, GGally, plot3D, plot3Drgl)
library(ggplot2)
theme_set(theme_bw())

noteTsne <- pca1 %>% 
  dplyr::select(-status) %>% ungroup()

noteTsne

noteTsne <- Rtsne(noteTsne, perplexity = 50, theta = 0, max_iter = 10000, verbose = T) #verbose=TURE可以看到跑的过程
noteTsne

noteTsne1 <- pca1 %>% dplyr::select(-area_hubei) %>% 
  mutate_if(.funs = scale, .predicate = is.numeric, scale = F) %>% 
  mutate(tSNE1 = noteTsne$Y[,1], tSNE2 = noteTsne$Y[,2]) %>% 
  pivot_longer(names_to = "Feature", values_to = "Value", c(-tSNE1, -tSNE2, -Status))

noteTsne1
#用来看原变量和新变量的关系
ggplot(noteTsne1, aes(tSNE1, tSNE2, col = Value, shape = Status)) +
  facet_wrap( ~ Feature) +
  geom_point(size = 2) +
  scale_color_gradient(low = "darkblue", high = "cyan") +
  theme_minimal()


#umap
pacman::p_load(tidyverse, mclust, Rtsne,umap,kohonen, lle, GGally, plot3D, plot3Drgl)

noteUmap <- pca1 %>% 
  dplyr::select(-status) %>% 
  as.matrix() %>% 
  umap(n_neibours = 7, min_dist = 0.1, 
       metric = "manhattan", n_epochs = 200, verbose = T)
#metrics euclidean 是欧氏距离 
noteUmap1 <- pca1 %>% 
  mutate_if(.funs = scale, .predicate = is.numeric, scale = F) %>% 
  mutate(UMAP1 = noteUmap$layout[,1], UMAP2 = noteUmap$layout[,2]) %>% 
  pivot_longer(names_to = "Feature", values_to = "Value", c(-UMAP1, -UMAP2, -status))


ggplot(noteUmap1, aes(UMAP1, UMAP2, col = Value, shape = status)) +
  facet_wrap(~ Feature) +
  geom_point(size = 2) +
  scale_color_gradient(low = "darkblue", high = "cyan")

#用umap可以知道假钞中也可以分为三类 说明假钞有三个来源 而sne只能没法在假钞中再区分 不管怎么调参数
