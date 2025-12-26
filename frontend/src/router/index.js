import { createRouter, createWebHashHistory } from 'vue-router'  // 确保正确导入
import EraDetail from '../components/EraDetail.vue'
import App from '../App.vue'  // 导入主组件

const router = createRouter({
  history: createWebHashHistory(),  // 使用哈希模式
  routes: [
    {
      path: '/',  // 添加根路径路由
      name: 'Home',
      component: App,  // 或者创建一个 Home 组件
      children: [
        // 这里可以添加子路由
      ]
    },
    {
      path: '/era/:eraId',
      name: 'EraDetail',
      component: EraDetail,
      props: true
    }
  ]
})

export default router