<template>
    <div class="homepage" style="margin-top: 6vh;">
      <!-- 第一部分 -->
      <div class="section section1">
        <div class="content">
          <div class="text">
            <p class="sub" style="color: black;">更便捷的一站式<br>房地产风险信息服务平台</p>
          </div>

          <div class="free">
            <el-button class="free-button" type="primary" style="width: 40%; font-size: 1.5vw; border-radius: 5px; height: 38px;" 
            @click="start"
            >开始使用&nbsp&nbsp<el-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-ea893728=""><path fill="currentColor" d="M754.752 480H160a32 32 0 1 0 0 64h594.752L521.344 777.344a32 32 0 0 0 45.312 45.312l288-288a32 32 0 0 0 0-45.312l-288-288a32 32 0 1 0-45.312 45.312z"></path></svg></el-icon></el-button>
          </div>
          
        </div>
      </div>

      <div class="section" ref="targetSection">
        <div style="display: flex; height: 100%; width: 100%; ">
          <div class="func">  
            <div class="cards" style="margin-left: 2%; ">  
              <div style="flex: 1; ">  
                <div class="text" style="margin-left: 30px; ">
                  <p class="sub" style="color: black; margin-bottom: 25px;">房企关联查询</p>
                  <p class="subtext" style="color: gray;">房地产企业信息，一键掌握</p> 
                  <el-button class="free-button" style="width: 35%; font-size: 1.5vw; border-radius: 5px; height: 38px;"
                   @click="companyLook">房地产关联查询&nbsp&nbsp<el-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-ea893728=""><path fill="currentColor" d="M754.752 480H160a32 32 0 1 0 0 64h594.752L521.344 777.344a32 32 0 0 0 45.312 45.312l288-288a32 32 0 0 0 0-45.312l-288-288a32 32 0 1 0-45.312 45.312z"></path></svg></el-icon></el-button>
                </div>
              </div>  
              <div class="imgs">  
                <img src="../assets/QQ截图20240311212543.png" alt="图">
              </div> 
            </div>  
          </div>
          <div class="func">
            <div class="cards" style="margin-right: 2%; ">  
              <div style="flex: 1; ">  
                <div class="text" style="margin-left: 30px; ">
                  <p class="sub" style="color: black; margin-bottom: 25px;">供应商风险查询</p>
                  <p class="subtext" style="color: gray;">供应商风险，一查便知</p> 
                  <el-button class="free-button" style="width: 40%; font-size: 1.5vw; border-radius: 5px; height: 38px;"
                   @click="riskLook">供应商风险查询&nbsp&nbsp<el-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-ea893728=""><path fill="currentColor" d="M754.752 480H160a32 32 0 1 0 0 64h594.752L521.344 777.344a32 32 0 0 0 45.312 45.312l288-288a32 32 0 0 0 0-45.312l-288-288a32 32 0 1 0-45.312 45.312z"></path></svg></el-icon></el-button>
                </div>
              </div>  
              <div class="imgs">  
                <img src="../assets/QQ截图20240311212543.png" alt="图">
              </div> 
            </div>  
          </div>
        </div>

      </div>

  
      <!-- 第四部分 -->
      <div class="section section4">
        <div class="content2">
          <div class="text" style="text-align: center;">
            <p class="sub" style="color: black; margin-top: 0; margin-bottom: 10vh;">成为会员</p>
          </div>

          <div class="plans">
            <div class="plan" >
              <div style="display: flex;">            
                <div style="flex: 1; margin-left: 20px; margin-top: 15px;">
                  <p style="color: black; font-weight: bold; font-size: 2vw;margin-top: 5px;margin-bottom: 15px;">个人版</p>
                  <p class="subtext">适合个人使用<br>无限次搜索<br>无限次下载</p>              
                </div>
                <div style="flex: 1;">
                  <p style="color: blue; font-weight: bold; font-size: 4.5vw; margin-top: 15px">29.9</p>
                  <p style="color: gray; font-size: 1.8vw; margin-top: 10px; text-align: center;">RMB/月</p>
                </div>
              </div>
              <div style="display: flex; justify-content: center; height: 6vh; margin-top: 10px">
                <el-button class="free-button" type="primary" style="margin-top: 0;width: 50%; font-size: 1.5vw; border-radius: 5px; height: 38px;" @click="upgrades">现在开通&nbsp&nbsp<el-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-ea893728=""><path fill="currentColor" d="M754.752 480H160a32 32 0 1 0 0 64h594.752L521.344 777.344a32 32 0 0 0 45.312 45.312l288-288a32 32 0 0 0 0-45.312l-288-288a32 32 0 1 0-45.312 45.312z"></path></svg></el-icon></el-button>
              </div>
            </div>

            <div class="plan" >
              <div style="display: flex;">            
                <div style="flex: 1; margin-left: 20px; margin-top: 15px;">
                  <p style="color: black; font-weight: bold; font-size: 2vw;margin-top: 5px;margin-bottom: 15px;">团队版</p>
                  <p class="subtext">适合团队使用<br>无限次搜索<br>无限次下载</p>              
                </div>
                <div style="flex: 1;">
                  <p style="color: blue; font-weight: bold; font-size: 4.5vw; margin-top: 15px">199.9</p>
                  <p style="color: gray; font-size: 1.8vw; margin-top: 10px; text-align: center;">RMB/月</p>
                </div>
              </div>
              <div style="display: flex; justify-content: center; height: 6vh; margin-top: 10px">
                <el-button class="free-button" type="primary" style="margin-top: 0;width: 50%; font-size: 1.5vw; border-radius: 5px; height: 38px;" @click="upgrades">现在开通&nbsp&nbsp<el-icon><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-ea893728=""><path fill="currentColor" d="M754.752 480H160a32 32 0 1 0 0 64h594.752L521.344 777.344a32 32 0 0 0 45.312 45.312l288-288a32 32 0 0 0 0-45.312l-288-288a32 32 0 1 0-45.312 45.312z"></path></svg></el-icon></el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div style="height: 6vh;width: 100%; display: flex; justify-content: center;  align-items: center; background-color: white;">
        版权所有&nbsp&nbsp&nbsp@花旗PropriskAI公司
      </div>
    </div>
  </template>
  
<style scoped>
.homepage {
  display: flex;
  flex-direction: column;
}

.section {
  height: 94vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
  color: white;
  text-align: center;
  /* font-size: 24px; */
  font-weight: bold;
  /* text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); */
}

.section1 {
  background-image: url('../assets/背景图.png');
  background-size: 100%;
  background-position: center; /* 可以确保背景图在容器内居中显示 */
}

.func {
  display: flex;
  flex: 1;
  height: 100%;
  justify-content: center;
  align-items: center;
}

.cards {
  height: 90%; 
  width: 90%; 
  box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.2);
  display: flex; 
  flex-direction: column;
  border-radius: 5px;
  ;background-color: rgba(255,255,255,0.7);
}

.imgs {
  flex: 2; 
  display: flex; 
  justify-content: center; 
  /* align-items: center; */
}

.imgs img {
  width: 90%; 
  height: 90%; 
  box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.2);
}

/* .section2 {
  background-color: white;
}*/
  
.section4 {
  /* background-color: white; */
} 

.content {
  max-width: 600px;
  margin-left: 10%; /* 距离页面最右边的距离 */
  margin-right: auto; 
}

.content2 {
  width: 53%;
}
.text {
  margin-bottom: 10px;
  text-align: left;
}
.text .sub {
  font-size: 2.5vw; 
}

.subtext {
  font-size: 1.5vw;
  margin-top: 3px;
  color: gray
}

.buttons {
  margin-bottom: 20px;
  text-align: left;
}

.content .free {
  text-align: left;
}

.free-button {
  background-color: rgb(69, 69, 250); /* 设置按钮背景颜色为蓝色 */
  color: white !important; /* 设置按钮文字颜色为白色 */
  border-color: blue; /* 设置按钮边框颜色为蓝色 */
  transition: background-color 0.3s; /* 添加过渡效果 */

  /* 悬停时颜色变浅蓝色 */
  /* &:hover {
    background-color: deepskyblue;
    border-color: deepskyblue;
  } */

  /* 点击时更浅 */
  &:active {
    background-color: lightblue;
    border-color: lightblue;
  }
}


.plans {
  display: flex;
  justify-content: center;
  width: 100%;
}

.plan {
  border-radius: 5px;
  text-align: left;
  margin: 0 10px;
  flex: 1;
  background-color: rgba(203, 217, 250, 0.4);
  box-shadow: 2px 4px 6px rgba(0, 0, 0, 0.2);
  /* display: flex; */
  width: 100%;
}

.plan p {
  margin-bottom: 10px;
}

.price_button {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: black
}



</style>
  
  
<script setup>
import {useStore} from 'vuex';
import bus from '../bus';
import {ref,onMounted} from 'vue'
import router from '../router';

const store=useStore()
const targetSection = ref(null);

const start=()=>{
  // 没有token
  if(!store.state.token) {
    bus.emit('/login')
    router.push({path:'/login'})
    return
  }
  // 获取视口的高度  
  const viewportHeight = window.innerHeight;  
  // 计算6vh的偏移量  
  const offset = viewportHeight * (6 / 100);  

  // 获取目标元素相对于视口的位置  
  const targetRect = targetSection.value.getBoundingClientRect();  

  // 计算新的滚动位置  
  const newScrollTop = targetRect.top - offset;  

  // 平滑滚动到新的位置  
  window.scrollTo({  
  top: newScrollTop,  
  behavior: 'smooth'  
  });
}

const companyLook=()=>{
  router.push({ path: '/realEstateSearch', query: { q: 'realEstateSearch' }})
  // router.push('/realEstateSearch')
}

const riskLook=()=>{
  router.push('/supplierSearch')
}

const upgrades=()=>{

}

</script>


  

  