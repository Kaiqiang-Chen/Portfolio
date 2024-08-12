<template>
        <div v-if="mode" class="container1">
            <div class="title1">登录 PropRiskAI</div>
            <el-input size="large" v-model="inputUsername" class="input1" placeholder=" 请输入账号"/>
            <el-input size="large" v-model="inputPassword" type="password" class="input2"  placeholder=" 请输入密码"/>
            <slideVerify ref="verify_slider" style="margin-top: 20px;margin-bottom: 20px;"></slideVerify>
            <el-button type="primary" class="button1" @click="login">
                登录
            </el-button>
            <el-text>还未注册？</el-text>
            <el-button type="primary" text @click="handleClickReg">立即注册</el-button>
        </div>
        <div v-else="mode" class="container1">
            <div class="title1">注册 PropRiskAI</div>
            <el-input size="large" v-model="inputUsernameReg" class="input1" placeholder=" 请输入账号"/>
            <el-input size="large" v-model="inputPasswordReg" type="password" class="input2"  placeholder=" 请输入密码"/>
            <el-input size="large" v-model="inputPasswordReg2" type="password" class="input3"  placeholder=" 请确认密码"/>
            <slideVerify ref="verify_slider" style="margin-top: 20px;margin-bottom: 20px;"></slideVerify>
            <el-button type="primary" class="button1" @click="register">
                注册
            </el-button>
            <el-text>已有帐号？</el-text>
            <el-button type="primary" text @click="handleClickReg">立即登录</el-button>
        </div>
</template>
<script setup lang="ts">
import {ref,onMounted} from 'vue'
let mode=ref(true)
import bus from '../bus';
import { ElMessage } from 'element-plus';
import slideVerify from './slideVerify.vue'
import axios from 'axios'
import { useRouter } from 'vue-router';
import {useStore} from 'vuex'
import {Md5} from 'ts-md5'

const router=useRouter()
let inputUsername=ref('')
let inputPassword=ref('')
let inputUsernameReg=ref('')
let inputPasswordReg=ref('')
let inputPasswordReg2=ref('')
const verified=ref(false)
const logined=ref(true)
const store=useStore()

defineExpose({
    slideVerify
})

bus.on('verified',(e)=>{
        verified.value=true
    })
bus.on('verify_refreshed',(e)=>{
        verified.value=false
    })

const handleClickReg=()=>{
    if(mode.value==true)
        mode.value=false
    else mode.value=true
    bus.emit('verify_refreshed','1')
}

const login=()=>{
        if(inputUsername.value==null||inputUsername.value=='')
        {
            ElMessage({
                showClose:true,
                message:'用户名不能为空',
                center:true,
                type:'error'
            })
            return
        }
        if(inputPassword.value==null||inputPassword.value=='')
        {
            ElMessage({
                showClose:true,
                message:'密码不能为空',
                center:true,
                type:'error'
            })
            return
        }
        if(!verified.value)
        {
            ElMessage({
                showClose:true,
                message:'请先完成验证',
                center:true,
                type:'error'
            })
            return
        }
        const url="http://127.0.0.1:5000/user_api/login"
        let encryptedPassword=Md5.hashStr(inputPassword.value)
        axios.post(url,{'username':inputUsername.value,'password':encryptedPassword}).then(res_data=>{
            store.state.token=res_data.data.token
            store.state.username=res_data.data.username
            store.state.role=res_data.data.role
            console.log(store.state.token)
            console.log(store.state.username)
            ElMessage({
                showClose:true,
                message:'登录成功',
                center:true,
                type:'success'
            })
            
            bus.emit('login_success','/home')
            router.push({path:'/home'})
        }).catch(error=>{
            ElMessage({
                showClose:true,
                message:error.response.data.message,
                center:true,
                type:'error'
            })
        })
        verified.value=false
        inputPassword.value=''
        bus.emit('verify_refresh','1')
}

const register=()=>{
    if(inputUsernameReg.value==null||inputUsernameReg.value=='')
        {
            ElMessage({
                showClose:true,
                message:'用户名不能为空',
                center:true,
                type:'error'
            })
            return
        }
        if(inputPasswordReg.value==null||inputPasswordReg.value=='')
        {
            ElMessage({
                showClose:true,
                message:'密码不能为空',
                center:true,
                type:'error'
            })
            return
        }
        if(inputPasswordReg.value!=inputPasswordReg2.value)
        {
            ElMessage({
                showClose:true,
                message:'确认密码与密码不符',
                center:true,
                type:'error'
            })
            
            inputPasswordReg2.value=''
            return

        }

        if(!verified.value)
        {
            ElMessage({
                showClose:true,
                message:'请先完成验证',
                center:true,
                type:'error'
            })
            return
        }        
        const url="http://127.0.0.1:5000/user_api/register"
        const encryptedPassword=Md5.hashStr(inputPasswordReg.value)
        axios.post(url,{'username':inputUsernameReg.value,'password':encryptedPassword}).then(res_data=>{
            store.state.token=res_data.data.token
            store.state.username=res_data.data.username
            store.state.role=res_data.data.role
            
            ElMessage({
                showClose:true,
                message:'注册成功',
                center:true,
                type:'success'
            })
            
            bus.emit('login_success','/home')
            router.push({path:'/home'})
        }).catch(error=>{
            ElMessage({
                showClose:true,
                message:error.response.data.message,
                center:true,
                type:'error'
            })
        })
        verified.value=false
        bus.emit('verify_refresh','1')
        inputPasswordReg.value=''
        inputPasswordReg2.value=''

}

</script>
<style scoped>
.container1{
    border-radius: 20px;
    background-color: white;
    margin: auto;
    padding: 100px;
    width:400px;
    margin-top: 100px;
}


.input1{
    border-radius: 15px;
    height: 50px;
    text-align: center;
    margin-top: 30px;
    margin-bottom: 5px;
}

.input2{
    
    border-radius: 15px;
    height: 50px;
    margin-bottom: 5px;
}

.input3{
    border-radius: 15px;
    height: 50px;
    margin-bottom: 10px;
}

.title1{
    text-align: center;
    font-weight: bold;
    font-size: 20px;

}

.button1{
    display: block;
    margin: auto;
    text-align: center;
    width: 100%;
    height: 50px;
    border-radius: 10px;
}

:deep(.el-input){
    --el-input-border-radius:10px
}
</style>