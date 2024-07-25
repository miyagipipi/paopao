import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createWebHistory, createRouter } from 'vue-router'
import routes from './router/route'
import 'vant/lib/index.css';
import { createPinia } from 'pinia'
import '@/global.css'
import VueVirtualScroller from 'vue-virtual-scroller'
import infiniteScroll from 'vue-infinite-scroll'


const router = createRouter({
  history: createWebHistory(),
  routes,
})


const app = createApp(App)
app.use(router)
app.use(createPinia())
app.use(VueVirtualScroller)
app.use(infiniteScroll)
app.mount('#app')
