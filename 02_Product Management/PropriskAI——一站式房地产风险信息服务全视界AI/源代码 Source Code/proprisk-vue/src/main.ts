
import { createApp } from 'vue'
import App from './App.vue'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import route from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import store from "./store"

const app=createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.use(ElementPlus)
app.use(route)
app.use(store)
app.mount('#app')