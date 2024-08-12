import{
    createRouter,
    createWebHistory
}from 'vue-router'

import realEstateSearch from "./components/realEstateSearch.vue"
import supplierSearch from "./components/supplierSearch.vue"
import login from "./components/login.vue"
import home from './components/home.vue'
import profile from './components/profile.vue'
import example from './components/example.vue'

const routes=[
    {
        path:'/home',
        component:home
    },
    {
        path:'/realEstateSearch',
        component:realEstateSearch
    },
    {
        path:'/supplierSearch',
        component:supplierSearch
    },
    {
        path:'/login',
        component:login
    },
    {
        path:'/',
        component:home
    },
    {
        path:'/profile',
        component:profile
    },
    {
        path: '/example',
        component: example
    }
]

const router=createRouter({history:createWebHistory(),routes})
export default router;