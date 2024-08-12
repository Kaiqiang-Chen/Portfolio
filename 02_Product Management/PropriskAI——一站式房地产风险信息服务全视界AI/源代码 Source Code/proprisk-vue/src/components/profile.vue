<template>
<div>
    <div class="container2">
        <div>
            当前用户：{{ store.state.username }}
        </div>
        <el-button type="primary" @click="logout" class="logout1">
            登出
        </el-button>
    </div>
</div>
</template>
<script setup lang="ts">
import { useStore } from 'vuex';
const store=useStore()
import router from '../router'

const logout=()=>{
    store.state.username=''
    store.state.token=''
    store.state.role=0
    router.push('/login')
}
</script>
<style scoped>

.container2{
    border-radius: 20px;
    background-color: white;
    margin: auto;
    padding: 100px;
    width:1000px;
    margin-top: 100px;
}

.logout1{
    margin: auto;
}

</style>
