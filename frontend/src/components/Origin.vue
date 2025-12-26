<template>
  <section>
    <!-- ① 3D 轮播 -->
    <section class="carousel-3d">
      <div class="stage">
        <div class="carousel" :style="{ transform: `rotateY(${-currAngle}deg)` }">
          <figure v-for="(m, i) in musicians" :key="m.key" class="card"
            :style="{ transform: `rotateY(${i * unit}deg) translateZ(${radius}px)` }">
            <div class="img-box" @click="toggleInfo(i)">
              <img :src="m.avatar" :alt="m.name" />
              <transition name="fade">
                <div v-if="showIdx === i" class="info-float" @click.stop>
                  <button class="close" @click="showIdx = null">✕</button>
                  <h4>{{ m.name }}</h4>
                  <p>{{ m.brief }}</p>
                  <p class="extra">{{ m.extra }}</p>
                </div>
              </transition>
            </div>
            <figcaption>{{ m.name }}</figcaption>
          </figure>
        </div>
      </div>

      <!-- 左右箭头 -->
      <el-button circle class="nav left" @click="rotate(1)">
        <el-icon>
          <ArrowLeft />
        </el-icon>
      </el-button>
      <el-button circle class="nav right" @click="rotate(-1)">
        <el-icon>
          <ArrowRight />
        </el-icon>
      </el-button>
    </section>

    <!-- ② 音乐发展史时间线 -->
    <MusicTimeline />
      <!-- 弹幕控制头部 -->
    <div class="danmu-header">
      <span>弹幕互动区</span>
      <span v-if="isLoadingDanmus" class="loading-text">加载弹幕中...</span>
      <button @click="loadDanmusFromBackend" class="refresh-btn" title="刷新弹幕">🔄</button>
    </div>
    <!-- ③ 弹幕区 -->
    <div class="danmu-box">
      <div v-for="t in 6" :key="t" class="track" :style="{ top: getTrackPosition(t) }">
        <transition-group name="dm" tag="div">
          <span v-for="d in trackPool[t]" :key="d.id" class="danmu" :style="{ '--speed': d.speed + 's' }"
            :data-user="d.isUser">
            {{ d.text }}
          </span>
        </transition-group>
      </div>
    </div>

    <!-- ④ 输入框 -->
    <div class="dm-control">
      <input v-model="input" @keyup.enter="sendDm" placeholder="输入弹幕内容..." class="dm-input" />
      <button class="dm-send" @click="sendDm">发送</button>
    </div>
  </section>
</template>

<script setup>
import MusicTimeline from './MusicTimeline.vue'
import { ref, reactive, onMounted, onUnmounted } from 'vue'

// 导入 ElementPlus 图标
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

/* ---------------- 3D 轮播 ---------------- */
const musicians = [
  { key: 'bach', name: 'J.S.巴赫', avatar: '/image/bahe.webp', brief: '巴洛克时期德国作曲家，被誉为"音乐之父"。', extra: '代表作：《平均律钢琴曲集》《勃兰登堡协奏曲》' },
  { key: 'mozart', name: 'W.A.莫扎特', avatar: '/image/mozhate.webp', brief: '古典主义奥地利天才作曲家。', extra: '代表作：《费加罗的婚礼》《第40交响曲》' },
  { key: 'beeth', name: 'L.v.贝多芬', avatar: '/image/beiduofen.webp', brief: '德国作曲家，古典→浪漫过渡人物。', extra: '代表作：《第九交响曲》《月光奏鸣曲》' },
  { key: 'chopin', name: 'F.肖邦', avatar: '/image/xiaobang.webp', brief: '浪漫主义波兰钢琴诗人。', extra: '代表作：《夜曲》《革命练习曲》' },
  { key: 'tchai', name: 'P.I.柴科夫斯基', avatar: '/image/chaikefusiji.jpg', brief: '俄国浪漫主义作曲家。', extra: '代表作：《天鹅湖》《第六交响曲》' },
  { key: 'debuss', name: 'C.德彪西', avatar: '/image/debiaoxi.jpg', brief: '法国印象派音乐奠基人。', extra: '代表作：《牧神午后前奏曲》《海》' }
]
const len = musicians.length
const unit = 360 / len
const radius = 280
let angle = 0
const currAngle = ref(0)
const showIdx = ref(null)

function toggleInfo(i) { showIdx.value = showIdx.value === i ? null : i }
function rotate(dir) { angle -= dir * unit; currAngle.value = angle }

/* ---------------- 弹幕系统 ---------------- */
const input = ref('')
const isLoadingDanmus = ref(false)

// 预定义的弹幕句子库
const sentenceBank = [
  '礼乐之邦，华夏正音', '高山流水，知音难觅', '霓裳羽衣，盛世华章', '诗经三百，皆可弦歌',
  '周公制礼作乐，天下归心', '孔子闻韶，三月不知肉味', '老子大音希声，大象无形', '骨笛九千年，声声吹古今',
  '编钟十二律，一钟双音妙', '唐大曲霓裳，飘然转旋回雪轻', '宋詞牌蝶恋，浅斟低唱杨柳岸',
  '元杂剧西厢，花月影中共婵娟', '明清皮黄, 京韵绕梁三日', '宫商角徵羽, 五音调心', '三分损益, 伶伦截竹',
  '律吕阴阳, 六律六吕', '琴瑟友之, 钟鼓乐之', '玉笛飞声, 散入春风', '谁家玉笛暗飞声', '散入春风满洛城',
  '此夜曲中闻折柳', '何人不起故园情'
]

// 用户自定义弹幕数组
const userSentences = reactive([])

// 合并所有弹幕源
const allSentences = reactive([...sentenceBank])

let idBase = 0
const trackPool = reactive({ 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] })

// ================ 只改这里：把15改成30 ================
const DANMU_SPEED = 30  // 弹幕速度：30秒走完（原来15秒）

// 添加用户弹幕到数组
function addUserSentence(text) {
  if (text && !allSentences.includes(text)) {
    allSentences.push(text)
    userSentences.push(text)
    console.log('用户弹幕已添加到本地库:', text)
  }
}

// 获取轨道位置
function getTrackPosition(trackNumber) {
  const trackHeight = 16.66
  const margin = 2
  return `calc(${(trackNumber - 1) * trackHeight + margin}% + 4px)`
}

// 从后端加载弹幕
const loadDanmusFromBackend = async () => {
  try {
    isLoadingDanmus.value = true
    console.log('📥 从后端加载弹幕...')
    
    const response = await fetch('http://localhost:5000/api/danmu?limit=30')
    const result = await response.json()
    
    if (result.success) {
      console.log(`✅ 加载了 ${result.count} 条弹幕`)
      
      // 清空现有的弹幕
      Object.keys(trackPool).forEach(key => {
        trackPool[key] = []
      })
      
      // 将后端弹幕添加到轨道池
      result.danmus.forEach((danmu, index) => {
        // 根据弹幕的position分配到对应轨道
        const track = danmu.position || 3
        const trackNum = Math.min(Math.max(1, track), 6)
        
        const dm = {
          id: `dm-backend-${danmu.id || index}`,
          text: danmu.text,
          speed: DANMU_SPEED,
          delay: 0,
          isUser: danmu.is_user || false
        }
        
        // 限制每个轨道的弹幕数量
        if (trackPool[trackNum].length < 5) {
          trackPool[trackNum].push(dm)
        }
      })
      
      console.log('弹幕加载完成，开始滚动...')
      
      // 启动弹幕发射器
      if (!window.danmuInterval) {
        fireLoop()
      }
    } else {
      console.error('❌ 加载弹幕失败:', result.message)
      initLocalDanmu()
    }
  } catch (error) {
    console.error('❌ 加载弹幕网络错误:', error)
    initLocalDanmu()
  } finally {
    isLoadingDanmus.value = false
  }
}

// 初始化本地弹幕（备用）
function initLocalDanmu() {
  console.log('使用本地弹幕句子库')
  Object.keys(trackPool).forEach(key => {
    trackPool[key] = []
  })
  
  sentenceBank.slice(0, 10).forEach((text, index) => {
    const track = (index % 6) + 1
    const dm = {
      id: `dm-local-${index}`,
      text: text,
      speed: DANMU_SPEED,
      delay: 0,
      isUser: false
    }
    
    if (trackPool[track].length < 3) {
      trackPool[track].push(dm)
    }
  })
  
  fireLoop()
}

// 弹幕发射函数
function pushSentence(track) {
  if (allSentences.length === 0) return

  const randomIndex = Math.floor(Math.random() * allSentences.length)
  const text = allSentences[randomIndex]
  const id = `dm-auto-${idBase++}`

  const dm = {
    id,
    text,
    speed: DANMU_SPEED,
    delay: 0,
    isUser: userSentences.includes(text)
  }

  trackPool[track].push(dm)

  setTimeout(() => {
    const idx = trackPool[track].findIndex(d => d.id === id)
    if (idx > -1) {
      trackPool[track].splice(idx, 1)
    }
  }, dm.speed * 1000)
}

// 随机发射器 - 只改这一行
function fireLoop() {
  if (window.danmuInterval) {
    clearInterval(window.danmuInterval)
  }
  
  const fireNext = () => {
    if (allSentences.length === 0) return
    
    const track = Math.floor(Math.random() * 6) + 1
    pushSentence(track)
  }
  
  fireNext()
  
  // ================ 只改这里：改成4000 ================
  window.danmuInterval = setInterval(fireNext, 4000)  // 4秒发一次弹幕
}

// 手动发送弹幕
async function sendDm() {
  const text = input.value.trim()
  if (!text) {
    alert('请输入弹幕内容！')
    return
  }

  if (text.length > 20) {
    alert('弹幕内容不能超过20个字！')
    return
  }

  try {
    const savedUser = localStorage.getItem('user')
    let userData = null
    let userId = null
    
    if (savedUser) {
      try {
        userData = JSON.parse(savedUser)
        userId = userData.id
      } catch (e) {
        console.error('解析用户数据失败:', e)
      }
    }
    
    const response = await fetch('http://localhost:5000/api/danmu', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
      },
      body: JSON.stringify({
        text: text,
        color: '#FFD700',
        position: 3,
        speed: DANMU_SPEED,
        user_id: userId
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      console.log('✅ 弹幕已保存到后端数据库:', text)
      
      addUserSentence(text)
      
      const track = 3
      const id = `dm-user-${Date.now()}`
      const dm = {
        id,
        text,
        speed: DANMU_SPEED,
        delay: 0,
        isUser: true
      }

      trackPool[track].push(dm)

      console.log('用户弹幕发送成功，轨道:', track, '内容:', text)

      setTimeout(() => {
        const idx = trackPool[track].findIndex(d => d.id === id)
        if (idx > -1) {
          trackPool[track].splice(idx, 1)
          console.log('用户弹幕完成显示，已从轨道移除:', text)
        }
      }, DANMU_SPEED * 1000)
      
    } else {
      console.error('❌ 弹幕保存失败:', result.message)
      addUserSentence(text)
      showLocalDanmu(text)
    }
  } catch (error) {
    console.log('❌ 弹幕保存失败，仅在前端显示:', error)
    addUserSentence(text)
    showLocalDanmu(text)
  }

  input.value = ''
}

// 在前端显示弹幕（备用）
function showLocalDanmu(text) {
  let track = 0
  const trackOrder = [3, 4, 2, 5, 1, 6]
  for (let t of trackOrder) {
    if (trackPool[t].length < 3) {
      track = t
      break
    }
  }
  if (track === 0) track = (idBase % 6) + 1

  const id = `dm-local-${Date.now()}`
  const dm = {
    id,
    text,
    speed: DANMU_SPEED,
    delay: 0,
    isUser: true
  }

  trackPool[track].push(dm)

  console.log('弹幕在前端显示，轨道:', track, '内容:', text)

  setTimeout(() => {
    const idx = trackPool[track].findIndex(d => d.id === id)
    if (idx > -1) {
      trackPool[track].splice(idx, 1)
    }
  }, DANMU_SPEED * 1000)
}

onMounted(() => {
  console.log('🎮 Origin组件已加载')
  loadDanmusFromBackend()
})

onUnmounted(() => {
  if (window.danmuInterval) {
    clearInterval(window.danmuInterval)
    window.danmuInterval = null
  }
})
</script>

<style scoped>
/* 弹幕控制头部 */
.danmu-header {
  margin: 0 20px 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #d4af37;
  font-size: 14px;
}

.loading-text {
  color: #aaa;
  font-style: italic;
  font-size: 12px;
}

.refresh-btn {
  background: rgba(212, 175, 55, 0.1);
  border: 1px solid #d4af37;
  color: #d4af37;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
}

.refresh-btn:hover {
  background: rgba(212, 175, 55, 0.2);
  transform: rotate(180deg);
}

/* ======== 3D 轮播 ======== */
.carousel-3d {
  position: relative;
  height: 420px;
  margin: 0 auto 40px;
  overflow: hidden;
}

.stage {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1200px;
}

.carousel {
  width: 200px;
  height: 250px;
  transform-style: preserve-3d;
  transition: transform .8s ease;
}

.card {
  position: absolute;
  width: 200px;
  height: 250px;
  backface-visibility: hidden;
  text-align: center;
}

.img-box {
  position: relative;
  display: inline-block;
}

.img-box img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, .4);
  cursor: pointer;
}

.card figcaption {
  margin-top: 8px;
  font-size: 16px;
  color: #d4af37;
}

.info-float {
  position: absolute;
  inset: 0;
  background: rgba(45, 45, 45, .95);
  border: 1px solid #d4af37;
  border-radius: 8px;
  color: #eee;
  padding: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.info-float h4 {
  color: #d4af37;
  margin: 0 0 6px;
}

.info-float .extra {
  font-size: 12px;
  color: #aaa;
  margin-top: 4px;
}

.info-float .close {
  position: absolute;
  top: 6px;
  right: 8px;
  background: none;
  border: none;
  color: #d4af37;
  cursor: pointer;
}

/* ElementPlus 按钮样式 */
:deep(.nav) {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, .5) !important;
  border: none !important;
  color: #fff !important;
  width: 36px !important;
  height: 36px !important;
  border-radius: 50% !important;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: .3s !important;
}

:deep(.nav:hover) {
  background: rgba(212, 175, 55, 0.8) !important;
  color: #000 !important;
}

:deep(.nav .el-icon) {
  font-size: 16px !important;
  font-weight: bold;
}
.nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
}
.nav.left {
  left: 10px; /* 调整为轮播图内部左侧 */
}

.nav.right {
  right: 10px; /* 调整为轮播图内部右侧 */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ======== 弹幕区域 ======== */
.danmu-box {
  position: relative;
  height: 140px;
  background: rgba(0, 0, 0, .3);
  border-radius: 8px;
  margin: 30px 20px 0 20px;
  overflow: hidden;
  border: 1px solid #444;
  width: calc(100% - 40px);
  padding: 8px 0;
}

.track {
  position: absolute;
  left: 0;
  right: 0;
  height: 14%;
  overflow: visible;
  display: flex;
  align-items: center;
}

.danmu {
  position: absolute;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  white-space: nowrap;
  line-height: 1.2;
  color: #fff;
  font-size: 14px;
  animation: dmMove var(--speed) linear forwards;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(212, 175, 55, 0.25);
  border: 1px solid rgba(212, 175, 55, 0.4);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 1;
  min-width: max-content;
  max-width: max-content;
}

/* 用户弹幕特殊样式 */
.danmu[data-user="true"] {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.7), rgba(255, 215, 0, 0.5));
  border: 2px solid #d4af37;
  color: #ffeb3b;
  font-weight: bold;
  box-shadow: 0 2px 12px rgba(212, 175, 55, 0.6);
  font-size: 15px;
}

@keyframes dmMove {
  0% {
    transform: translateY(-50%) translateX(0);
    left: 100%;
  }
  100% {
    transform: translateY(-50%) translateX(calc(-100vw - 200px));
    left: 0;
  }
}

.dm-enter-active {
  animation: dmEnter 0.5s ease-out;
}

.dm-leave-active {
  animation: dmLeave 0.5s ease-in;
}

@keyframes dmEnter {
  0% {
    opacity: 0;
    transform: translateY(-50%) translateX(120%);
  }
  100% {
    opacity: 1;
    transform: translateY(-50%) translateX(0);
  }
}

@keyframes dmLeave {
  0% {
    opacity: 1;
    transform: translateY(-50%) translateX(calc(-100vw - 200px));
  }
  100% {
    opacity: 0;
    transform: translateY(-50%) translateX(calc(-100vw - 250px));
  }
}

/* ======== 输入框 ======== */
.dm-control {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 15px 20px 0 20px;
  padding: 0;
}

.dm-input {
  flex: 1;
  background: rgba(45, 45, 45, 0.8);
  border: 1px solid #d4af37;
  color: #eee;
  outline: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s;
  min-width: 200px;
}

.dm-input:focus {
  border-color: #ffeb3b;
  box-shadow: 0 0 12px rgba(212, 175, 55, 0.6);
  background: rgba(45, 45, 45, 0.9);
}

.dm-input::placeholder {
  color: #888;
}

.dm-send {
  padding: 10px 24px;
  background: linear-gradient(135deg, #d4af37, #ffd700);
  color: #000;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s;
  min-width: 80px;
}

.dm-send:hover {
  background: linear-gradient(135deg, #ffd700, #ffeb3b);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
}

.dm-send:active {
  transform: translateY(0);
}
</style>