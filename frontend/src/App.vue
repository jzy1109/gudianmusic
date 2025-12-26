<template>
  <div id="app" class="page">
    <!-- 登录页面 -->
    <Login v-if="!isLoggedIn" @login-success="handleLoginSuccess" />

    <!-- 已登录的主页面 -->
    <div v-else>
      <!-- 头部 -->
      <header class="head">
        <h1>古典音乐</h1>
        <p>传承千年音律之美 · 探寻华夏音乐之魂</p>

        <!-- 用户信息和退出按钮 -->
        <div class="user-info">
          <span class="welcome-text">欢迎，{{ currentUser.username }}</span>
          <button class="logout-btn" @click="handleLogout">
            <span class="logout-icon">🚪</span> 退出登录
          </button>
        </div>
      </header>

      <!-- 导航栏 -->
      <nav class="nav">
        <button v-for="t in tabs" :key="t.id" @click="switchTab(t.id)" :class="{ active: currentTab === t.id }">
          <span class="tab-icon">{{ getTabIcon(t.id) }}</span>
          {{ t.name }}
        </button>
      </nav>

      <!-- 主要内容区域 -->
      <main class="main-content">
        <!-- 路由出口 -->
        <router-view v-if="$route.name === 'EraDetail'"></router-view>

        <!-- 标签页内容 -->
        <keep-alive v-else>
          <div class="tab-content">
            <!-- 动态组件 -->
            <component :is="comMap[currentTab]" :collectList="collectList" @toggle-favorite="toggleFavorite" />
          </div>
        </keep-alive>
      </main>

      <!-- 页脚 -->
      <footer class="footer">
        <div class="footer-content">
          <div class="footer-left">
            <h3>古典音乐 · 让传统活在当下</h3>
            <p>探索千年音乐文化，感受华夏音律之美</p>
          </div>

          <div class="footer-right">
            <p style="margin: 4px 0; text-align: right;">后端服务状态:
              <span :class="{ online: isBackendOnline }" style="color: #4CAF50;" v-if="isBackendOnline">在线</span>
              <span :class="{ online: isBackendOnline }" style="color: #f44336;" v-else>离线</span>
            </p>
            <p style="margin: 4px 0; text-align: right;">当前用户:
              <span style="color: #d4af37;">{{ currentUser.username }}</span>
            </p>
          </div>
        </div>
        <div class="copyright">
          © 2025 古典音乐网站 | 基于Vue 3 + Flask构建
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
/* 新增：全局收藏接口 */
import { getFavorites, addFavorite, delFavorite } from './api/favorite.js'
import Login from './components/Login.vue'
import Origin from './components/Origin.vue'
import Instr from './components/Instr.vue'
import Theory from './components/Theory.vue'
import Gallery from './components/Gallery.vue'
import Collect from './components/Collect.vue'

// ========== 1. 路由实例 ==========
const route = useRoute()
const router = useRouter()

// ========== 2. 响应式数据 ==========
const isLoggedIn = ref(false)
const isBackendOnline = ref(false)
const currentUser = ref({ username: '访客', id: null })

// 标签页配置
const tabs = [
  { id: 'origin', name: '音乐起源' },
  { id: 'instr', name: '传统乐器' },
  { id: 'theory', name: '音乐理论' },
  { id: 'gallery', name: '作品长廊' },
  { id: 'collect', name: '我的收藏' }
]

// 当前选中的标签页
const currentTab = ref('origin')

// 全局收藏列表（唯一真相）
const collectList = ref([])

// 统一拉取收藏
async function syncCollect() {
  const res = await getFavorites()
  if (res.success) collectList.value = res.list
}

// 子组件可调用：收藏/取消后立刻刷新全局
async function toggleFavorite(item) {
  const existed = collectList.value.some(i => i.key === item.key)
  const promise = existed ? delFavorite(item) : addFavorite(item)
  const ok = await promise
  if (ok.success) await syncCollect()
}

// 组件映射
const comMap = {
  origin: Origin,
  instr: Instr,
  theory: Theory,
  gallery: Gallery,
  collect: Collect
}

// ========== 3. 标签初始化（刷新不跳回起源） ==========
const initialTab = window.__INITIAL_TAB__ || localStorage.getItem('lastTab')
currentTab.value = initialTab && comMap[initialTab] ? initialTab : 'origin'

// 保存当前标签页到本地存储
watch(currentTab, (newTab) => {
  localStorage.setItem('lastTab', newTab)
})

// 检查路由变化并更新当前标签页
watch(route, (newRoute) => {
  if (newRoute.name === 'EraDetail') {
    currentTab.value = 'origin'
  }
})

// ========== 4. 本地存储相关 ==========
const STORAGE_KEY = 'music_collections'

// 从本地存储加载收藏数据
const loadCollections = () => {
  try {
    const savedData = localStorage.getItem(STORAGE_KEY)
    if (savedData) {
      collectList.value = JSON.parse(savedData)
      console.log('📂 从本地存储加载收藏数据:', collectList.value.length, '项')
    }
  } catch (error) {
    console.error('加载收藏数据失败:', error)
  }
}

// 保存收藏数据到本地存储
const saveCollections = () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(collectList.value))
    console.log('💾 收藏数据已保存到本地存储')
  } catch (error) {
    console.error('保存收藏数据失败:', error)
  }
}

// 检查本地登录状态
const checkLocalLoginStatus = () => {
  console.log('🔐 检查本地登录状态...')
  const savedUser = localStorage.getItem('user')
  const savedToken = localStorage.getItem('token')
  if (savedUser && savedToken) {
    try {
      const userData = JSON.parse(savedUser)
      console.log('✅ 找到本地保存的用户:', userData.username)
      isLoggedIn.value = true
      currentUser.value = { username: userData.username, id: userData.id }
      return true
    } catch (error) {
      console.error('解析用户数据失败:', error)
      clearLocalStorage()
      return false
    }
  } else {
    console.log('🔓 本地没有登录信息')
    isLoggedIn.value = false
    currentUser.value = { username: '访客', id: null }
    return false
  }
}

// 清理本地存储
const clearLocalStorage = () => {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  localStorage.removeItem('rememberedUser')
  console.log('🧹 本地存储已清理')
}

// 处理登录成功
const handleLoginSuccess = (userData) => {
  console.log('🎉 登录成功事件触发:', userData)
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try {
      const userData = JSON.parse(savedUser)
      isLoggedIn.value = true
      currentUser.value = { username: userData.username, id: userData.id }
      console.log('✅ 登录状态已更新:', userData.username)
    } catch (error) {
      console.error('解析用户数据失败:', error)
    }
  }
}

// 处理退出登录
const handleLogout = () => {
  console.log('🚪 用户请求退出登录')
  clearLocalStorage()
  isLoggedIn.value = false
  currentUser.value = { username: '访客', id: null }
  console.log('✅ 退出登录成功')
  collectList.value = []
  currentTab.value = 'origin'
  if (route.name !== 'Home') router.push('/')
}

// 切换标签页
function switchTab(tabId) {
  console.log(`🔄 切换标签页: ${currentTab.value} -> ${tabId}`)
  currentTab.value = tabId
  localStorage.setItem('lastTab', tabId)
  if (route.name === 'EraDetail') router.push('/')
}

// 获取标签页图标
function getTabIcon(tabId) {
  const icons = { origin: '🎵', instr: '🎻', theory: '📚', gallery: '🖼️', collect: '❤️' }
  return icons[tabId] || '📄'
}

// 检查后端服务状态
const checkBackendStatus = async () => {
  console.log('🔍 检查后端服务状态...')
  try {
    const res = await fetch('http://localhost:5000/api/hello', { headers: { Accept: 'application/json' } })
    isBackendOnline.value = res.ok
    console.log(isBackendOnline.value ? '✅ 后端服务在线' : '❌ 后端服务响应异常')
  } catch (e) {
    isBackendOnline.value = false
    console.log('❌ 无法连接到后端服务:', e.message)
  }
}

// ========== 8. 生命周期 ==========
onMounted(() => {
  checkBackendStatus()
  checkLocalLoginStatus()
  loadCollections()
  syncCollect()          // 首次进入拉收藏
  watch(collectList, () => saveCollections(), { deep: true })
})

onUnmounted(() => {
  // 清理逻辑
})
</script>

<style scoped>
/* 基础样式 */
.page {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: #1a1a1a;
  color: #eee;
  font-family: STKaiti, KaiTi, serif;
  display: flex;
  flex-direction: column
}

/* 头部 */
.head {
  text-align: center;
  padding: 25px 0 20px;
  border-bottom: 2px solid #d4af37;
  background: rgba(26, 26, 29, .95);
  position: relative
}

.head h1 {
  font-size: 48px;
  color: #d4af37;
  margin-bottom: 6px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, .5)
}

.head p {
  font-size: 16px;
  color: #ccc;
  margin: 0;
  letter-spacing: 1px
}

.user-info {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 15px
}

.welcome-text {
  color: #d4af37;
  font-size: 14px;
  padding: 6px 12px;
  background: rgba(212, 175, 55, .1);
  border-radius: 4px;
  border: 1px solid rgba(212, 175, 55, .3)
}

.logout-btn {
  padding: 8px 16px;
  background: rgba(212, 175, 55, .1);
  border: 1px solid #d4af37;
  color: #d4af37;
  border-radius: 4px;
  cursor: pointer;
  transition: all .3s;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px
}

.logout-btn:hover {
  background: #d4af37;
  color: #000;
  transform: translateY(-1px)
}

.logout-icon {
  font-size: 14px
}

/* 导航 */
.nav {
  display: flex;
  justify-content: center;
  border-bottom: 1px solid #444;
  padding: 0 20px;
  background: rgba(45, 45, 45, .9);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100
}

.nav button {
  padding: 14px 24px;
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
  transition: all .3s;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  margin: 0 2px
}

.nav button:hover {
  color: #d4af37;
  background: rgba(212, 175, 55, .05)
}

.nav button.active {
  color: #d4af37;
  border-bottom: 2px solid #d4af37;
  font-weight: bold
}

.nav button.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #d4af37, transparent)
}

.tab-icon {
  font-size: 18px
}

/* 主内容 */
.main-content {
  flex: 1;
  padding: 30px 20px;
  min-height: 60vh
}

.tab-content {
  animation: fadeIn .5s ease
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px)
  }

  to {
    opacity: 1;
    transform: translateY(0)
  }
}

/* 页脚 */
.footer {
  background: #1a1a1a;
  border-top: 1px solid #444;
  padding: 30px 20px 20px;
  margin-top: 40px
}

.footer-right {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-end !important
}

.footer-right p {
  margin: 4px 0 !important;
  text-align: right !important;
  line-height: 1.5 !important
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  max-width: 1200px;
  margin: 0 auto 20px;
  flex-wrap: wrap;
  gap: 30px
}

.footer-left h3 {
  color: #d4af37;
  margin-bottom: 10px;
  font-size: 20px
}

.footer-left p {
  color: #888;
  font-size: 14px;
  margin: 0
}

.footer-right p {
  color: #aaa;
  font-size: 14px;
  margin: 5px 0
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px
}

.status-indicator.online {
  background: #4CAF50;
  box-shadow: 0 0 8px #4CAF50
}

.status-indicator:not(.online) {
  background: #f44336;
  box-shadow: 0 0 8px #f44336
}

.copyright {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #333;
  color: #666;
  font-size: 12px
}

/* 响应式 */
@media (max-width:768px) {
  .head h1 {
    font-size: 36px
  }

  .user-info {
    position: static;
    justify-content: center;
    margin-top: 15px
  }

  .nav {
    flex-wrap: wrap
  }

  .nav button {
    padding: 10px 15px;
    font-size: 14px
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
    gap: 20px
  }

  .footer-left,
  .footer-right {
    width: 100%
  }
}

@media (max-width:480px) {
  .head h1 {
    font-size: 28px
  }

  .head p {
    font-size: 14px
  }

  .nav button {
    padding: 8px 12px;
    font-size: 13px
  }

  .tab-icon {
    font-size: 16px
  }

  .main-content {
    padding: 20px 10px
  }
}
</style>