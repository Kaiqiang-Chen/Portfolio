<template>
    <div class="container1">
        <el-icon style="color:rgb(90,105,245);vertical-align: -15%;" :size="25"><OfficeBuilding /></el-icon>
        <el-text class="title1">
            查找供应商风险
        </el-text>
        <div class="container2">
            <el-input
            v-model="inputsupplier"
            class="searchBox1"
            size="large"
            placeholder="输入供应商企业名称或者组织代码"
            :prefix-icon="Search"
            clearable=true
            id="searchBox1"
            />
            <el-button type="primary" class="searchButton1" color="rgb(61,78,244)" 
                        style="color: rgb(255,255,255) ;"
                        @click="handlesupplierSearch">搜索</el-button>
        </div>
        
        <el-table
        :data="realEstateData"
        :key="refreshNum1"
        :border="true"
        :stripe="true"
        empty-text="暂无数据"
        style="width: 100%; border-top-left-radius: 10px; border-top-right-radius: 10px; margin-top: 20px;">
            <el-table-column prop="realEstateName" label="关联交易房地产企业">
              <template #="scope">
                <el-button type="text" @click="handleJumpToRealEstateSearch(scope.row.realEstateName)">
                  {{ scope.row.realEstateName }}

                </el-button>
              </template>
            </el-table-column>
            <el-table-column prop="realEstateCode" label="股票代码"/>
            <el-table-column label="影响">
                <template #="scope">
                        <span>
                            {{scope.row.realEstateAffection}}
                        </span>
                </template>
            </el-table-column>
        </el-table>
    </div>
    <div class="container3">
        <el-icon style="color:rgb(90,105,245);vertical-align: -15%;" :size="25"><InfoFilled /></el-icon>
        <el-text class="title1">
            供应商详情
        </el-text>
        <div class="unlock-message" v-if="store.state.role==0||store.state.role==null">
          解锁详细报告需开通会员 </div>
        <div :class="{mask:store.state.role==0||store.state.role==null}">
          
        <div class="discription1">
            <el-text size="large" class="detailStyle">
                {{ supplierDetail }}
            </el-text>
        </div>
        <p class="title2">当前风险等级</p>
          <p class="title3">*风险结合房地产公司拖欠供应商应付账款和供应商总收入等来衡量</p>
        <div id="diagram1" class="diagram2">
        </div>
        <div id="diagram2" class="diagram1">
        </div>
        <div id="diagram3" class="diagram1">
        </div>
        <div id="diagram4" class="diagram1">
        </div>
        <div id="diagram5" class="diagram1">
        </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import {InfoFilled, Search } from '@element-plus/icons-vue'
import {ref,onMounted} from 'vue'
import axios from 'axios'
import { useStore } from 'vuex';
import {ElLoading} from 'element-plus'
const store = useStore();
import * as echarts from 'echarts'
import "echarts-liquidfill"
import {ElMessage} from "element-plus";
import bus from '@/bus';
import router from '@/router';
let inputsupplier=ref('')
let refreshNum1=ref(0)
class realEstateDataRow{
    realEstateName;
    realEstateCode;
    realEstateAffection;
    constructor(realEstateName:string,realEstateCode:string,realEstateAffection:number)
    {
        this.realEstateName=realEstateName;
        this.realEstateCode=realEstateCode;
        this.realEstateAffection=realEstateAffection
    }
}
let riskLevel:number=20
let realEstateData:realEstateDataRow[]=[]
let realEstateNameList:string[]=[]
let realEstateAffectionList:number[]=[]
let isLoadingTable1=ref(false)
let yearList1:string[]=[]
let revenueList:number[]=[]
let yearList2:string[]=[]
let profitList:number[]=[]
let yearList3:string[]=[]
let cashFlowList:number[]=[]
let yearList4:string[]=[]
let ROEList:number[]=[]

const handlesupplierSearch=()=>{
    let supplier=inputsupplier.value;
    const url="http://127.0.0.1:5000/supplierSearch"
    isLoadingTable1.value=true
    const token=store.state.token
    console.log(token)
    const loading=ElLoading.service({
      lock:true,
      text:'正在加载，稍等几秒就好',
      background:'rgba(0,0,0,0.5)'
    })
    const config={headers:{'Authorization':token}}
    axios.post(url,{supplier:supplier},config).then(responseData=>{
        loading.close()
        realEstateData=responseData.data.supplierResult;
        console.log(responseData.data)
        refreshNum1.value=Math.random();
        isLoadingTable1.value=false
        supplierDetail.value=responseData.data.supplierDiscription
        // riskLevel=responseData.data.riskLevel
        console.log(responseData.data.affected_degree[0]['value'])
        riskLevel=responseData.data.affected_degree[0]['value']*100
        diagram1Option.series[0].data=[riskLevel / 100]
        diagram1Option.title.text=[String(riskLevel)+"%\n"+calcRisk()+"风险"].join("")
        if(50<riskLevel&&riskLevel<=100)
        {
          diagram1Option.series[0].itemStyle.color.colorStops=[
                  {
                    offset: 0,
                    color: ["rgba(230, 50, 50, 1)"], // 0% 处的颜色
                  },
                  {
                    offset: 1,
                    color: ["rgba(255, 180, 180, 1)"], // 100% 处的颜色
                  },
                ]
          
        }
        else if(20<riskLevel&&riskLevel<=50)
        {
          diagram1Option.series[0].itemStyle.color.colorStops=[
                  {
                    offset: 0,
                    color: ["rgba(240, 240, 40, 1)"], // 0% 处的颜色
                  },
                  {
                    offset: 1,
                    color: ["rgba(255, 255, 180, 1)"], // 100% 处的颜色
                  },
                ]
        }
        else
        {
          diagram1Option.series[0].itemStyle.color.colorStops=[
                  {
                    offset: 0,
                    color: ["rgba(230, 240, 90, 1)"], // 0% 处的颜色
                  },
                  {
                    offset: 1,
                    color: ["rgba(230, 245, 90, 1)"], // 100% 处的颜色
                  },
                ]
        }


        console.log(riskLevel)
        // realEstateNameList=[]
        // realEstateAffectionList=[]
        // for(var i=0;i<realEstateData.length;i++)
        // {
        //     realEstateNameList.push(realEstateData[i].realEstateName)
        //     realEstateAffectionList.push(realEstateData[i].realEstateAffection)
        // }
        // diagram2Option.yAxis.data=realEstateNameList.reverse()
        // diagram2Option.series[0].data=realEstateAffectionList.reverse()
        yearList1=[]
        revenueList=[]
        for(var i=0;i<responseData.data.supplier_revenue.length;i++)
        {
          yearList1.push(responseData.data.supplier_revenue[i].year)
          revenueList.push(responseData.data.supplier_revenue[i].value)
        }

        yearList2=[]
        profitList=[]
        for(var i=0;i<responseData.data.supplier_profit.length;i++)
        {
          yearList2.push(responseData.data.supplier_profit[i].year)
          profitList.push(responseData.data.supplier_profit[i].value)
        }

        yearList3=[]
        cashFlowList=[]
        for(var i=0;i<responseData.data.supplier_cash_flow.length;i++)
        {
          yearList3.push(responseData.data.supplier_cash_flow[i].year)
          cashFlowList.push(responseData.data.supplier_cash_flow[i].value)
        }

        yearList4=[]
        ROEList=[]
        for(var i=0;i<responseData.data.supplier_ROE.length;i++)
        {
          yearList4.push(responseData.data.supplier_ROE[i].year)
          ROEList.push(responseData.data.supplier_ROE[i].value)
        }

        diagram2Option.xAxis.data=yearList1.reverse()
        diagram2Option.series[0].data=revenueList.reverse()
        diagram3Option.xAxis.data=yearList2.reverse()
        diagram3Option.series[0].data=profitList.reverse()
        diagram4Option.xAxis.data=yearList3.reverse()
        diagram4Option.series[0].data=cashFlowList.reverse()
        diagram5Option.xAxis.data=yearList4.reverse()
        diagram5Option.series[0].data=ROEList.reverse()
        initDiagram()
    }).catch(error=>{
      loading.close()
      ElMessage({
            showClose:true,
            message:error.response.data.message,
            center:true,
            type:'error'
        })
    })
}

const handleJumpToRealEstateSearch=(row:string)=>{

  router.push('/realEstateSearch')
  bus.emit('jumpToRealEstateSearch',row)
  console.log(row)
}

bus.on('jumpToSupplierSearch',(data)=>{
  inputsupplier.value=data
  handlesupplierSearch()
})

const calcRisk=()=>{
  if(0<=riskLevel&&riskLevel<=20)return "低"
  else if(20<riskLevel&&riskLevel<=50)return "中"
  else if(50<riskLevel&&riskLevel<=100)return "高"
  else return ""
}


// const updateDiagram=()=>{
//     diagram1.setOption(diagram1Option)
//     diagram2.setOption(diagram2Option)
//     diagram3.setOption(diagram3Option)
//     diagram4.setOption(diagram4Option)
// }


const initDiagram=()=>{

    echarts.dispose(document.getElementById('diagram1'))
    let diagram1=echarts.init(document.getElementById('diagram1'))
    diagram1.setOption(diagram1Option)
    
    echarts.dispose(document.getElementById('diagram2'))
    let diagram2=echarts.init(document.getElementById('diagram2'))
    diagram2.setOption(diagram2Option)
    
    echarts.dispose(document.getElementById('diagram3'))
    let diagram3=echarts.init(document.getElementById('diagram3'))
    diagram3.setOption(diagram3Option)

    echarts.dispose(document.getElementById('diagram4'))
    let diagram4=echarts.init(document.getElementById('diagram4'))
    diagram4.setOption(diagram4Option)

    echarts.dispose(document.getElementById('diagram5'))
    let diagram5=echarts.init(document.getElementById('diagram5'))
    diagram5.setOption(diagram5Option)
}

let supplierDetail=ref('暂无描述')
let diagram1Option={
        title: {
          text: [String(riskLevel)+"%\n"+calcRisk()+"风险"].join(""),//'\n'换行，主标题
          textStyle: {//主标题文字的样式
            rich: {//在 rich 里面，可以自定义富文本样式。利用富文本样式，可以在标签中做出非常丰富的效果。例子：formatter: ['{a|这段文本采用样式a}','{b|这段文本采用样式b}这段用默认样式{x|这段用样式x}'].join('\n')
              a: {
                fontSize: 22,
              },
            },
            color: "#E2F8FF",
            fontSize: 20,
            lineHeight: 24,
            fontWeight: 400,
          },
          subtextStyle: {fontSize: 20},//副标题文字的样式
          left: "center",
          top: "center",//title 组件离容器上侧的距离。
        },
        series: [
          {
            type: "liquidFill",
            center: ["50%", "50%"],
            radius: "60%",
            data: [riskLevel / 100],
            direction: "right", //波浪的方向｛left right none}
            outline: {
              show: true, //是否显示轮廓 布尔值
              borderDistance: 15, // 外部边框与图表的距离 数字
              itemStyle: {
                borderColor: {
                  // 边框的颜色
                  type: "linear",
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [
                    {
                      offset: 0,
                      color: ["rgba(32, 128, 223,1)"], // 0% 处的颜色
                    },
                    {
                      offset: 0.5,
                      color: ["rgba(62, 146, 226,0.7)"], // 0% 处的颜色
                    },
                    {
                      offset: 1,
                      color: ["rgba(6, 11, 30, 0.5)"], // 100% 处的颜色
                    },
                  ],
                  global: false, // 缺省为 false
                },
                borderWidth: 1, // 边框的宽度
                shadowOffsetX: 0,
                shadowOffsetY: 8,
                shadowColor: "#000000", //外部轮廓的阴影颜色
              },
            },
            itemStyle: {
              opacity: 0.8, // 波浪的透明度·
              shadowBlur: 0, // 波浪的阴影范围
              color: {
                type: "linear",
                x: 0,
                y: 1,
                x2: 0,
                y2: 0,
                colorStops: [
                  {
                    offset: 0,
                    color: ["rgba(102, 240, 150, 1)"], // 0% 处的颜色
                  },
                  {
                    offset: 1,
                    color: ["rgba(102, 245, 217, 1)"], // 100% 处的颜色
                  },
                ],
                global: false, // 缺省为 false
              },
            },
            backgroundStyle: {
              color: {
                type: "radial",
                x: 0.5,
                y: 0.5,
                r: 0.5,
                colorStops: [
                  {
                    offset: 0,
                    color: ["rgba(20, 50, 70,1)"], // 0% 处的颜色
                  },
                  {
                    offset: 0.6,
                    color: ["rgba(34, 84, 124, 1)"], // 60% 处的颜色
                  },
                  {
                    offset: 0.93,
                    color: ["rgba(64, 127, 191, 1)"], // 93% 处的颜色
                  },
                  {
                    offset: 1,
                    color: ["rgba(51, 254, 255, 0.8)"], // 100% 处的颜色
                  },
                ],
                global: false, // 缺省为 false
              },
            },
            label: {
              // 数据展示样式
              show: false,
            },
          },
        ],
      };
                   
let diagram2Option = {
  title: {
    text: '收入预测',
    left: 'center'
  },  
  grid: {
    left: '10%',
    right: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [150, 230, 224, 218, 135, 147, 260],
      type: 'line',
      connectNulls: true
    }
  ]
};

let diagram3Option = {
  title: {
    text: '利润预测',
    left: 'center'
  },  
  grid: {
    left: '10%',
    right: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [150, 230, 224, 218, 135, 147, 260],
      type: 'line',
      connectNulls: true
    }
  ]
};

let diagram4Option = {
  title: {
    text: '现金流预测',
    left: 'center'
  },  
  grid: {
    left: '10%',
    right: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [150, 230, 224, 218, 135, 147, 260],
      type: 'bar',
      connectNulls: true
    }
  ]
};

let diagram5Option = {
  title: {
    text: '净资产收益率',
    left: 'center'
  },  
  grid: {
    left: '10%',
    right: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [150, 230, 224, 218, 135, 147, 260],
      type: 'bar',
      connectNulls: true
    }
  ]
};

onMounted(()=>{
    initDiagram()
})



</script>
<style scoped>
.container1{
    border-radius: 20px;
    background-color: white;
    margin: auto;
    padding: 40px;
    width:1000px;
    margin-top: 80px;
    white-space:nowrap ;
}

.container3{
    border-radius: 20px;
    background-color: white;
    margin: auto;
    padding: 40px;
    width:1000px;
    margin-top: 25px;
    white-space:nowrap ;
    z-index: 0;
    position: relative;
}

.container2{
    flex-direction: row;
    justify-content: center;
}

.title1{
    font-weight: bold;
    font-size: 25px;
}

.searchBox1{
    margin: auto;
    width: 80%;
    margin-top: 20px;
    margin-bottom: 10px;
}

.searchButton1{
    height: 40px;
    width: 100px;
    margin-left: 50px;
    border-radius: 6px;
    margin-top: 20px;
    margin-bottom: 10px;
}

:deep(.el-input){
    --el-input-border-color:transparent;
    --el-input-hover-border-color:rgb(223, 215, 208);
    --el-input-focus-border-color:rgb(150,160,249);
    --el-input-placeholder-color:rgb(175, 169, 162);
    --el-input-border-radius:8px;
    --el-input-text-color:rgb(109, 84, 58);
}

:deep(.el-input__inner){
    background-color: rgb(248,247,246);
    border-color: transparent;
}

:deep(.el-input__wrapper){
    background-color: rgb(248,247,246);
}

:deep(.el-button){
    --el-button-text-color:
}

:deep(.el-main){
    --el-main-padding:0px;
}

:deep(.el-table)
{
    --el-table-header-bg-color:rgb(241,246,255)
}

.detailStyle{
  word-break:break-all;
  white-space: normal;
  word-wrap: break-word;
}

.discription1{
    margin-top: 15px;
    margin-bottom: 25px;
}

.diagram1{
    margin:auto;
    width: 800px;
    height: 500px;    
}

.diagram2{    
    margin:auto;
    width: 600px;
    height: 400px; 
}

.title2{
    margin: auto;
    font-size: 19px;
    font-weight: bold;
    color: rgb(70,70,70);
    text-align: center;
}

.title3{
  margin: auto;
  font-size: 13px;
  opacity: 0.7;
  text-align: center;
}

.mask{
  filter: blur(10px);
  position: relative;
  z-index: 0;
}

.unlock-message{
  font-size: 25px;
  text-align: center;
  color: black;
  position: absolute;
  transform: translate(-50%, -50%);
  z-index: 1;
  top:200px;
  left: 50%;
  right: 0;
  padding: 20px;
  padding:10px;

}

</style>