<template>
  <div class="menu-container">
    <el-menu
      :default-active="route.path"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#FFFFFF"
      text-color="#000000"
      :ellipsis="false"
      @select="handleSelect"
      active-text-color="#3d4ef4"
      :router="true"
      :font-size="25"
    >
      <img src="../assets/2.PNG"></img>
      <div class="flex-grow"></div>
      <el-menu-item index="/home">首页</el-menu-item>
      <el-menu-item index="/realEstateSearch">房企关联查询</el-menu-item>
      <el-menu-item index="/supplierSearch">供应商风险查询</el-menu-item>
      <el-menu-item index="/example">案例</el-menu-item>
      <el-menu-item v-if="store.state.username==''||store.state.username==null" index="/login">登录</el-menu-item>
      <el-menu-item v-else index="/profile">用户信息</el-menu-item>
    </el-menu>
  </div>

  <div>
    <keep-alive>
      <router-view v-slot="{ Component }">
          <component :is="Component" />
      </router-view>
    </keep-alive>
  </div>
</template>

<script setup lang="ts">
import { ref, KeepAlive } from 'vue'
import { onMounted } from 'vue';
import bus from '../bus';
import {useRoute} from 'vue-router'
import { useStore } from 'vuex';

const store=useStore()
const route=useRoute()

let defaultActiveIndex = ref('/home')

const handleSelect = (key: string, keyPath: string[]) => {
  sessionStorage.setItem('currentPath', key)
  console.log(key, keyPath)
}

onMounted(() => {
  defaultActiveIndex.value = sessionStorage.getItem('currentPath') || '/home'
})

bus.on('login_success', (e) => {
  defaultActiveIndex.value = '/realEstateSearch'
})

bus.on('jumpToRealEstateSearch',(e)=>{
  defaultActiveIndex.value = '/realEstateSearch'
})

bus.on('jumpToSupplierSearch',(e)=>{
  defaultActiveIndex.value = '/supplierSearch'
})

</script>

<style>
.menu-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999; /* Ensure it's above other content */
}

.logo {
  color: #000000;
  font-weight: bold;
  font-size: 17px;
}

.logo2{
  height: px;

}

.flex-grow {
  flex-grow: 1;
}

.el-main {
  --el-main-padding: 0px !important;
}
</style>
