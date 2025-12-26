<template>
  <section>
    <h2>我的收藏</h2>
    <!-- 第2章-条件渲染 -->
    <div v-if="!list || list.length === 0" class="empty">
      暂无收藏，快去乐器页/长廊/理论页添加吧！
    </div>
    <div v-else class="clist">
      <!-- 第2章-列表渲染 -->
      <div v-for="c in list" :key="c.key" class="citem">
        <span class="icon">{{ c.icon }}</span>
        <div class="txt">
          <h3>{{ c.name }}</h3>
          <p>{{ c.brief }}</p>
          <!-- 第2章-条件渲染和样式绑定 -->
          <div v-if="c.type === 'work' && currentPlaying === c.key" class="progress">
            <div class="progress-bar" :style="{ width: progress + '%' }"></div>
          </div>
        </div>

        <!-- 播放按钮 -->
        <button class="play" @click="togglePlay(c)" :class="{ on: currentPlaying === c.key }">
          {{ getPlayButtonText(c) }}
        </button>

        <!-- 移除按钮 -->
        <button @click="remove(c)">移除</button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, onDeactivated, onActivated } from 'vue'
import { getFavorites } from '../api/collect.js'

// 收藏列表（来自 MySQL）
const list = ref([])

onMounted(async () => {
  const res = await getFavorites()
  if (res.success) list.value = res.list
  console.log('🎵 Collect组件已加载', 'MySQL 收藏数:', list.value.length)
})

// 播放/暂停（保持你原来逻辑）
let audioContext = null
let melodyTimeouts = []
const currentPlaying = ref(null)
const isPlaying = ref(false)
const progress = ref(0)
let progressInterval = null
let totalDuration = 0
let startTime = 0

function stopCurrentSound() {
  melodyTimeouts.forEach(t => clearTimeout(t))
  melodyTimeouts = []
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
  currentPlaying.value = null
  isPlaying.value = false
  progress.value = 0
  totalDuration = 0
  startTime = 0
}

function playWorkMelody(item) {
  stopCurrentSound()
  currentPlaying.value = item.key
  isPlaying.value = true
  // 这里用你原来写好的旋律数据即可，key 匹配就行
  const melody = [
    { note: 'C4', duration: 0.8 }, { note: 'D4', duration: 0.6 }, { note: 'E4', duration: 1.2 },
    { note: 'G4', duration: 0.6 }, { note: 'A4', duration: 0.6 }, { note: 'G4', duration: 1.2 },
    { note: 'E4', duration: 0.6 }, { note: 'D4', duration: 0.6 }, { note: 'C4', duration: 2.0 }
  ]
  const noteFrequencies = {
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00
  }
  let currentTime = 0
  totalDuration = melody.reduce((sum, n) => sum + n.duration, 0) * 1000
  startTime = Date.now()
  progressInterval = setInterval(() => {
    const elapsed = Date.now() - startTime
    progress.value = Math.min((elapsed / totalDuration) * 100, 100)
    if (progress.value >= 100) clearInterval(progressInterval)
  }, 100)

  melody.forEach(noteData => {
    const timeout = setTimeout(() => {
      if (currentPlaying.value === item.key && isPlaying.value) {
        playNote(noteFrequencies[noteData.note], noteData.duration, 'sine')
      }
    }, currentTime)
    melodyTimeouts.push(timeout)
    currentTime += noteData.duration * 1000
  })

  const endTimeout = setTimeout(() => {
    if (currentPlaying.value === item.key) stopCurrentSound()
  }, currentTime)
  melodyTimeouts.push(endTimeout)
}

function playNote(frequency, duration, type = 'sine') {
  const context = new (window.AudioContext || window.webkitAudioContext)()
  const osc = context.createOscillator()
  const gain = context.createGain()
  osc.type = type
  osc.frequency.setValueAtTime(frequency, context.currentTime)
  gain.gain.setValueAtTime(0, context.currentTime)
  gain.gain.linearRampToValueAtTime(0.3, context.currentTime + 0.05)
  gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + duration * 0.8)
  osc.connect(gain).connect(context.destination)
  osc.start(context.currentTime)
  osc.stop(context.currentTime + duration)
}

function togglePlay(item) {
  if (currentPlaying.value === item.key) {
    stopCurrentSound()
  } else {
    playWorkMelody(item)
  }
}

function getPlayButtonText(item) {
  return currentPlaying.value === item.key ? '暂停' : '播放'
}

// 移除收藏
async function remove(item) {
  // 调后端删除
  await fetch('http://localhost:5000/api/favorites', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${JSON.parse(localStorage.getItem('user') || '{}').id}` },
    body: JSON.stringify({ type: item.type, key: item.key })
  })
  // 本地列表同步
  list.value = list.value.filter(i => i.key !== item.key)
  // 如果正在播放就停掉
  if (currentPlaying.value === item.key) stopCurrentSound()
}

// 生命周期
onUnmounted(stopCurrentSound)
onDeactivated(stopCurrentSound)
onActivated(stopCurrentSound)
</script>

<style scoped>
.clist {
  display: grid;
  gap: 12px
}

.citem {
  display: flex;
  align-items: center;
  background: #2d2d2d;
  border-radius: 8px;
  padding: 16px;
  gap: 12px;
  position: relative;
}

.citem .icon {
  font-size: 32px;
  flex-shrink: 0;
}

.citem .txt {
  flex: 1;
  min-width: 0;
}

.citem .txt h3 {
  color: #d4af37;
  margin-bottom: 4px;
  font-size: 16px;
}

.citem .txt p {
  color: #ccc;
  font-size: 13px;
  margin: 0 0 8px 0;
}

.progress {
  width: 100%;
  height: 4px;
  background: #444;
  border-radius: 2px;
  overflow: hidden;
  margin-top: 8px;
}

.progress-bar {
  height: 100%;
  background: #d4af37;
  transition: width 0.1s linear;
  border-radius: 2px;
}

.citem button.play,
.citem button {
  background: none;
  border: 1px solid #d4af37;
  color: #d4af37;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: .3s;
  flex-shrink: 0;
  font-size: 12px;
  white-space: nowrap;
}

.citem button.play:hover,
.citem button:hover {
  background: #d4af37;
  color: #000;
}

.citem button.play.on {
  background: #d4af37;
  color: #000;
}

.empty {
  text-align: center;
  padding: 60px 0;
  color: #666;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .citem {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }

  .citem .txt {
    width: 100%;
  }

  .citem .audio-controls {
    display: flex;
    gap: 8px;
    width: 100%;
  }

  .citem button.play,
  .citem button {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .citem {
    padding: 12px;
  }

  .citem .icon {
    font-size: 24px;
  }
}
</style>