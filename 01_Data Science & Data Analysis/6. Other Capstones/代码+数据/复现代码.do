*** 陈凯强_did论文复现——《碳市场的碳减排效应研究》*** 
ssc install reghdfe 
ssc install ftools
ssc install coefplot
ssc install dpplot

clear
cd C:\Users\10136\Desktop\大三下\课程\商业数据分析\论文复现_陈凯强（代码+数据）
use data_0.dta 
//数据说明：Raw Data文件夹中是原始数据（为后续表合并等的方便稍经处理），利用python生成1_数据大表，再用excel进行一些处理后得到最终使用的数据表——0_最终数据表。（处理过程见各个raw data文件和Data Cleasing中的Python代码）
//把最终数据表另存到成data.dta并且在运行代码时使用，其他的dta都是运行时生成的

**多期DID处理变量构建**

**北京（pro=4），天津（pro=7），上海（pro=1），重庆（pro=27），湖北（pro=21），广东（pro=12），福建（pro=24），深圳（city=169），四川（pro=6）**
gen treatment=(pro==4|pro==7|pro==1|pro==27|pro==21|pro==12|pro==24)
gen post=1 if (pro==4|pro==7|pro==1|pro==12) & year>=2013
replace post=1 if (pro==27|pro==21) & year>=2014
replace post=1 if pro==24 & year>=2016
replace post=0 if post!=1
gen DID=treatment*post
save data.dta,replace

**控制变量设置全局宏方便后续分析，可以在后续的命令中通过引用这个宏（$controlvars）来一次性使用所有的这些变量，而不需要每次都列出所有的变量名**
global controlvars "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1 t2 t3"

**设置面板数据**
xtset city year,yearly

**1. 基准回归**
//reghdfe用于估计具有多个高维固定效应的线性模型// //控制区域、城市、区域城市交互固定效应//

//不加控制变量，碳市场机制对碳排放总量有抑制作用，但不显著
reghdfe lnco2 DID,absorb(city year region#year) vce(cluster pro) 
//加控制变量，碳市场对碳排放有抑制作用，且显著
reghdfe lnco2 DID $controlvars ,absorb(city year region#year) vce(cluster pro) 
//不加控制变量，系数显著为负，碳市场机制对碳排放有显著的抑制作用
reghdfe lncogdp DID, absorb(city year region#year) vce(cluster pro)
//加控制变量，系数绝对值增大，显著性增强
reghdfe lncogdp DID $controlvars , absorb(city year region#year) vce(cluster pro)


**2. 平行趋势检验，对应附表4**
clear
use "data.dta"

//生成政策节点与政策处理交互项//
gen tpilot=2013 if city==169
replace tpilot=2013 if pro==1
replace tpilot=2013 if pro==4
replace tpilot=2013 if pro==7
replace tpilot=2013 if pro==12 & city!=169
replace tpilot=2014 if pro==21
replace tpilot=2014 if pro==27
replace tpilot=2016 if pro==24

gen policy=year-tpilot if treatment==1

tab policy //生成policy的频率表//
forvalues i=10(-1)1{
    gen pre_`i'=(policy==-`i') //政策前期虚拟变量
	}
gen current=(policy==0) //政策当期虚拟变量

forvalues i=1(1)4{
    gen post_`i'=(policy==`i') //政策后期虚拟变量
	}
	 
drop pre_10 pre_9 pre_8 pre_7 //因为多重共线性丢弃四个组

//平行趋势检验图//
reghdfe lnco2 pre_* current post* $controlvars c.c_int#c.lnpgdp, absorb(city year region#year) vce(cluster pr)
coefplot,baselevels keep(pre_* current post*) vertical yline(0) ytitle("二氧化碳排放量回归系数") xtitle("各期动态效应") addplot(line @b @at)
ciopts(recast(rcap)) scheme(s1mono) //keep 保留前面回归中哪些变量的系数;ciopts是置信区间；recast(rcap)是置信区间样式；scheme是配色

reghdfe lncogdp pre_* current post* $controlvars c.c_int#c.lnpgdp, absorb(city year region#year) vce(cluster pr)
coefplot,baselevels keep(pre_* current post*) vertical yline(0) ytitle("二氧化碳排放强度回归系数") xtitle("各期动态效应") addplot(line @b @at)
ciopts(recast(rcap)) scheme(s1mono)


**安慰剂检验**
//按照作者所说将重抽样次数设置为500，对三个变量分别做重抽样；:后面是重抽样后要跑的回归
permute DID _b[DID],reps(500) rseed(2023) saving("policy_1.dta",replace):reghdfe lnco2 DID $controlvars, absorb(city year region#year) vce(cluster pro)
permute DID _b[DID],reps(500) rseed(2023)saving("policy_2.dta",replace):reghdfe lncogdp DID $controlvars, absorb(city year region#year) vce(cluster pro)
permute treatment _b[c.treatment#c.post],reps(500) rseed(2023)saving("group_1.dta",replace):reghdfe lnco2 c.treatment#c.post $controlvars , absorb(city year region#year)vce(cluster pro)
permute treatment _b[c.treatment#c.post],reps(500) rseed(2023)saving("group_2.dta",replace):reghdfe lncogdp c.treatment#c.post $controlvars , absorb(city year region#year)vce(cluster pro)
permute post _b[c.treatment#c.post],reps(500) rseed(2023)saving("post_1.dta",replace):reghdfe lnco2 c.treatment#c.post $controlvars, absorb(city year region#year)vce(cluster pro)
permute post _b[c.treatment#c.post],reps(500) rseed(2023)saving("post_2.dta",replace):reghdfe lncogdp c.treatment#c.post $controlvars, absorb(city year region#year)vce(cluster pro)

//画核密度图
use"policy_1.dta",clear
dpplot _pm_1,xline(-0.0833,lc(black*0.5) lp(solid)) 
xline(0,lc(black*0.5)lp(dash))
xtitle("Estimator",size(*0.8))
xlabel(-0.1(0.025)0.1,format(%4.3f)labsize(small))
ytitle("Density",size(*0.8))
ylabel(,nogrid format(%4.1f) labsize(small))
note("") caption("") graphregion(fcolor(white))
xsize(8)
ysize(5)

use"policy_2.dta",clear
dpplot _pm_1,xline(-0.0833,lc(black*0.5) lp(solid)) 
xline(0,lc(black*0.5)lp(dash))
xtitle("Estimator",size(*0.8))
xlabel(-0.1(0.025)0.1,format(%4.3f)labsize(small))
ytitle("Density",size(*0.8))
ylabel(,nogrid format(%4.1f) labsize(small))
graphregion(fcolor(white))
xsize(8)
ysize(5)

use"group_1.dta",clear
dpplot _pm_1,xline(-0.0833,lc(black*0.5) lp(solid)) 
xtitle("Estimator",size(*0.8))
xlabel(-0.1(0.025)0.1,format(%4.3f)labsize(small))
ytitle("Density",size(*0.8))
ylabel(,nogrid format(%4.1f) labsize(small))
graphregion(fcolor(white))
xsize(8)
ysize(5)

use"group_2.dta",clear
dpplot _pm_1,xline(-0.0833,lc(black*0.5) lp(solid)) 
xline(0,lc(black*0.5)lp(dash))
xtitle("Estimator",size(*0.8))
xlabel(-0.1(0.025)0.1,format(%4.3f)labsize(small))
ytitle("Density",size(*0.8))
ylabel(,nogrid format(%4.1f) labsize(small))
graphregion(fcolor(white))
xsize(8)
ysize(5)

use"post_1.dta",clear
dpplot _pm_1,xline(-0.0833,lc(black*0.5) lp(solid)) 
xline(0,lc(black*0.5)lp(dash))
xtitle("Estimator",size(*0.8))
xlabel(-0.1(0.025)0.1,format(%4.3f)labsize(small))
ytitle("Density",size(*0.8))
ylabel(,nogrid format(%4.1f) labsize(small))
graphregion(fcolor(white))
xsize(8)
ysize(5)

use"post_2.dta",clear
dpplot _pm_1,xline(-0.0833,lc(black*0.5) lp(solid)) 
xline(0,lc(black*0.5)lp(dash))
xtitle("Estimator",size(*0.8))
xlabel(-0.1(0.025)0.1,format(%4.3f)labsize(small))
ytitle("Density",size(*0.8))
ylabel(,nogrid format(%4.1f) labsize(small))
graphregion(fcolor(white))
xsize(8)
ysize(5)

// 通过抽样，发现不存在安慰剂效应（和原始回归系数相差大）



**稳健性检验：剔除其他政策和特殊地域影响**



**稳健性检验1、PSM DID 倾向性得分匹配 有两种 一种是所有时间段放在一起匹配，一种是逐年匹配 这里用逐年匹配**

**法1：半径匹配，2006-2010，只保留匹配上的城市**

***2006***
use "data.dta",clear
keep if year==2006
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) radius cal(0.05) ate ties logit common
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2006.dta",replace

***2007***
use "data.dta",clear
keep if year==2007
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) radius cal(0.05) ate ties logit common
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2007.dta",replace
 
***2008***
use "data.dta",clear
keep if year==2008
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) radius cal(0.05) ate ties logit common
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2008.dta",replace


***2009***
use "data.dta",clear
keep if year==2009
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) radius cal(0.05) ate ties logit common
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2009.dta",replace

***2010***
use "data.dta",clear
keep if year==2010
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) radius cal(0.05) ate ties logit common
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2010.dta",replace

***合并前面匹配上的城市***
merge 1:1 city using "psm_2009.dta",keep(3)nogen
merge 1:1 city using "psm_2008.dta",keep(3)nogen
merge 1:1 city using "psm_2007.dta",keep(3)nogen
merge 1:1 city using "psm_2006.dta",keep(3)nogen
save "psm_total.dta",replace

***psm合并文件再和主回归文件合并***
use "data.dta",clear
merge m:1 city using "psm_total.dta",keep(3)nogen
xtset ci year
reghdfe lnco2 DID $controlvars , absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID $controlvars , absorb(city year region#year)vce(cluster pro)

reghdfe lnco2 DID $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID $controlvars, absorb(city year region#year)vce(cluster pro)

**法2：近邻匹配，2006-2010，只保留匹配上的城市**
***2006***
use "data.dta",clear
keep if year==2006
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) logit ate neighbor(4) common ties //改变的是这里的参数，别的和前面一样//
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2006_n.dta",replace

***2007***
use "data.dta",clear
keep if year==2007
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) logit ate neighbor(4) common ties 
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2007_n.dta",replace
 
***2008***
use "data.dta",clear
keep if year==2008
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) logit ate neighbor(4) common ties 
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2008_n.dta",replace


***2009***
use "data.dta",clear
keep if year==2009
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) logit ate neighbor(4) common ties 
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2009_n.dta",replace

***2010***
use "data.dta",clear
keep if year==2010
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) logit ate neighbor(4) common ties 
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2010_n.dta",replace

***同样，合并前面匹配上的城市***
merge 1:1 city using "psm_2009_n.dta",keep(3)nogen
merge 1:1 city using "psm_2008_n.dta",keep(3)nogen
merge 1:1 city using "psm_2007_n.dta",keep(3)nogen
merge 1:1 city using "psm_2006_n.dta",keep(3)nogen
save "psm_total_n.dta",replace

***同样，psm合并文件再和主回归文件合并***
use "data.dta",clear
merge m:1 city using "psm_total_n.dta",keep(3)nogen
xtset ci year
reghdfe lnco2 DID $controlvars , absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID $controlvars , absorb(city year region#year)vce(cluster pro)

reghdfe lnco2 DID $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID $controlvars, absorb(city year region#year)vce(cluster pro)


**法3：核匹配 kernal ，2006-2010，只保留匹配上的城市**
***2006***
use "data.dta",clear
keep if year==2006
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) kernel ate logit common ties //改变的是这里的参数，别的和前面一样//
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2006_k.dta",replace

***2007***
use "data.dta",clear
keep if year==2007
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) kernel ate logit common ties 
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2007_k.dta",replace
 
***2008***
use "data.dta",clear
keep if year==2008
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) kernel ate logit common ties 
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2008_k.dta",replace


***2009***
use "data.dta",clear
keep if year==2009
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) kernel ate logit common ties  
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2009_k.dta",replace

***2010***
use "data.dta",clear
keep if year==2010
set seed 2023
gen tmp=runiform()
sort tmp
global control "lnpgdp lnpgdpp strind strser strls strwz popden lnpop marketindex lnqys strsq strpub lnslfd lnzls t1"
psmatch2 pilot $control ,out(lnco2) kernel ate logit common ties 
pstest $control,both
gen common=_support
drop if common==0|common==.
keep city
save "psm_2010_k.dta",replace

***同样，合并前面匹配上的城市***
merge 1:1 city using "psm_2009_k.dta",keep(3)nogen
merge 1:1 city using "psm_2008_k.dta",keep(3)nogen
merge 1:1 city using "psm_2007_k.dta",keep(3)nogen
merge 1:1 city using "psm_2006_k.dta",keep(3)nogen
save "psm_total_k.dta",replace

***同样，psm合并文件再和主回归文件合并***
use "data.dta",clear
merge m:1 city using "psm_total_k.dta",keep(3)nogen
xtset ci year
reghdfe lnco2 DID $controlvars , absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID $controlvars , absorb(city year region#year)vce(cluster pro)

reghdfe lnco2 DID $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID $controlvars, absorb(city year region#year)vce(cluster pro)


**稳健性检验2 剔除其他政策影响**

use data.dta,clear
//lnco2//
reghdfe lnco2 DID $controlvars if lc2010==1|lc2012==1|lc2017==1,absorb(city year region#year) vce(cluster pro)
reghdfe lnco2 DID $controlvars if city47==1,absorb(city year region#year) vce(cluster pro)
reghdfe lnco2 DID $controlvars if sopilot,absorb(city year region#year) vce(cluster pro)
//lncogdp//
reghdfe lncogdp DID $controlvars if lc2010==1|lc2012|lc2017==1,absorb(city year region#year) vce(cluster pro)
reghdfe lncogdp DID $controlvars if city47==1,absorb(city year region#year) vce(cluster pro)
reghdfe lncogdp DID $controlvars if sopilot,absorb(city year region#year) vce(cluster pro)

*** 稳健性检验3 剔除特殊地区影响 ***
//lnco2//
reghdfe lnco2 DID $controlvars if pro!=4&pro!=1&city!=169,absorb(city year region#year) vce(cluster pro)
reghdfe lnco2 DID $controlvars if pro!=27,absorb(city year region#year) vce(cluster pro)
reghdfe lnco2 DID $controlvars if pro!=6,absorb(city year region#year) vce(cluster pro)
//lncogdp//
reghdfe lncogdp DID $controlvars if pro!=4&pro!=1&city!=169,absorb(city year region#year) vce(cluster pro)
reghdfe lncogdp DID $controlvars if pro!=27,absorb(city year region#year) vce(cluster pro)
reghdfe lncogdp DID $controlvars if pro!=6,absorb(city year region#year) vce(cluster pro)


**机制分析**

** 1. 市场运行状况 **

//lnco2//
reghdfe lnco2 DID c.DID#C.lnprice $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lnco2 DID c.DID#C.lnliqui $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lnco2 DID c.DID#C.strvol $controlvars, absorb(city year region#year)vce(cluster pro)

//lncngdp//
reghdfe lncogdp DID c.DID#C.lnprice $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID c.DID#C.lnliqui $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID c.DID#C.strvol $controlvars, absorb(city year region#year)vce(cluster pro)

** 2. 政府干预效应 **
gen penalty=6 if pro==1|city==169|pro==4
replace penalty=5 if pro==27
replace penalty=4 if pro==21
replace penalty=3 if pro==12&city!=169
replace penalty=2 if pro==24
replace penalty=1 if pro==7
replace penalty=0 if penal==.
replace penalty=0 if DID==0

//lnco2//
reghdfe lnco2 DID c.DID#C.strgygz $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lnco2 DID c.DID#C.strpub $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lnco2 DID c.DID#C.penalty $controlvars, absorb(city year region#year)vce(cluster pro)
//lncogdp//
reghdfe lncogdp DID c.DID#C.strgygz $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID c.DID#C.strpub $controlvars, absorb(city year region#year)vce(cluster pro)
reghdfe lncogdp DID c.DID#C.penalty $controlvars, absorb(city year region#year)vce(cluster pro)

