import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
// 提前恢复路由，防止闪现首页
const savedPath = localStorage.getItem('lastRoute');
if (savedPath && savedPath !== '/') {
  // 先临时把路径写进地址栏，Vue Router 会立即识别
  history.replaceState(null, null, savedPath);
}
const lastTab = localStorage.getItem('lastTab')
if (lastTab) {
  // 让 App.vue 能通过 inject 拿到
  window.__INITIAL_TAB__ = lastTab
}
const app = createApp(App);
app.use(router); // 第5章 路由 - Vue Router 的使用
app.use(ElementPlus); // 第6章 - Element Plus 集成
app.mount('#app');