<template>
    <section class="theory-grid">
        <!-- ① 五声调式 -->
        <div class="box">
            <h2>五声调式</h2>
            <div class="keys">
                <!-- 第2章-列表渲染和样式绑定 -->
                <button v-for="(s, i) in wuyin" :key="i" @click="playWuyin(i)" class="tone-play"
                    :class="{ playing: currentPlaying === `wuyin-${i}` }">
                    {{ s.name }}
                </button>
            </div>
            <p>宫商角徵羽，对应 Do Re Mi Sol La，没有半音，旋律平和。</p>

            <!-- 收藏按钮 -->
            <!-- 第2章-计算属性和样式绑定 -->
            <button @click="toggleTone" :class="['btn-collect', { collected: isToneCollected }]">
                {{ isToneCollected ? '已收藏' : '收藏五声调式' }}
            </button>
        </div>

        <!-- ② 十二律吕 -->
        <div class="box">
            <h2>十二律吕</h2>
            <div class="lulu">
                <!-- 第2章-列表渲染 -->
                <span v-for="(l, i) in lulu" :key="l" @click="playLulu(i)"
                    :class="{ playing: currentPlaying === `lulu-${i}` }">
                    {{ l }}
                </span>
            </div>
            <p>六律六吕，共十二半音，相传为伶伦竹管定律。</p>
        </div>

        <!-- ③ 互动测验 -->
        <div class="box full">
            <h2>互动测验</h2>
            <p>{{ cur.q }}</p>
            <div class="quiz">
                <!-- 第2章-列表渲染 -->
                <button v-for="a in cur.ans" :key="a" @click="check(a)">{{ a }}</button>
            </div>
            <button @click="next" class="next">换一题</button>
            <!-- 第4章-动画过渡 -->
            <transition name="fade">
                <p v-if="tip" class="tip">{{ tip }}</p>
            </transition>
        </div>
    </section>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onActivated, onUnmounted } from 'vue'
import { getFavorites, addFavorite, delFavorite } from '../api/favorite.js'

// 第3章-子组件向父组件传递数据
const emit = defineEmits(['update:collectList'])
// 第3章-父组件向子组件传递数据
const props = defineProps({
    collectList: { type: Array, default: () => [] }
})

/* 与数据库同步收藏状态 */
async function syncCollectedStatus() {
  const res = await getFavorites()
  if (!res.success) return

  const collectedKeys = new Set(res.list.map(i => i.key))
  // 五声调式的 key 固定为 theory-wuyin
  isToneCollected.value = collectedKeys.has('theory-wuyin')

  // 同时把最新列表抛给父组件，保证 Collect.vue 实时
  const newCollectList = res.list
  emit('update:collectList', newCollectList)
}

onMounted(() => {
  syncCollectedStatus()
})

onActivated(() => {
  syncCollectedStatus()
})

/* ================= 音频上下文和工具 ================= */
// Web Audio API 集成
let audioContext = null
let currentOscillator = null
const currentPlaying = ref(null)

// 初始化音频上下文
function initAudioContext() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)()
    }
}

// 清理音频资源
function stopCurrentSound() {
    if (currentOscillator) {
        currentOscillator.stop()
        currentOscillator = null
    }
    currentPlaying.value = null
}

// 生成音调
function playTone(frequency, duration = 1.0, type = 'sine', key = '') {
    initAudioContext()
    stopCurrentSound()

    currentPlaying.value = key

    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()

    // 设置波形
    oscillator.type = type
    oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime)

    // 设置音量包络 - 更自然的衰减
    gainNode.gain.setValueAtTime(0, audioContext.currentTime)
    gainNode.gain.linearRampToValueAtTime(0.3, audioContext.currentTime + 0.1)
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration)

    // 连接节点
    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)

    // 开始播放
    oscillator.start(audioContext.currentTime)

    currentOscillator = oscillator

    // 自动停止
    setTimeout(() => {
        stopCurrentSound()
    }, duration * 1000)
}

// 组件卸载时清理
// 第3章-生命周期函数
onUnmounted(() => {
    stopCurrentSound()
})

/* ---------------- 五声调式 ---------------- */
const wuyin = [
    { name: '宫', frequency: 261.63 },  // C4
    { name: '商', frequency: 293.66 },  // D4
    { name: '角', frequency: 329.63 },  // E4
    { name: '徵', frequency: 392.00 },  // G4
    { name: '羽', frequency: 440.00 }   // A4
]

function playWuyin(i) {
    const note = wuyin[i]
    if (note) {
        playTone(note.frequency, 1.5, 'sine', `wuyin-${i}`)
    }
}

const toneKey = 'theory-wuyin'

/* 收藏 / 取消收藏 */
async function toggleTone() {
  const key = 'theory-wuyin'
  const oldStatus = isToneCollected.value

  // 乐观更新
  isToneCollected.value = !oldStatus

  const item = {
    type: 'theory',
    key,
    name: '五声调式',
    icon: '🎵',
    brief: '宫商角徵羽 · Do Re Mi Sol La'
  }

  const promise = oldStatus ? delFavorite(item) : addFavorite(item)
  const res = await promise

  if (res.success) {
    // 成功后再同步一次（保险）
    await syncCollectedStatus()
  } else {
    // 失败回滚
    isToneCollected.value = oldStatus
    ElMessage.error(res.message || '操作失败')
  }
}

// 第2章-计算属性
const isToneCollected = ref(false)

/* ---------------- 十二律吕 ---------------- */
// 十二律吕频率 (基于黄钟=261.63Hz，按三分损益法计算)
const luluFrequencies = [
    261.63,  // 黄钟 (C)
    277.18,  // 大吕 (C#)
    293.66,  // 太簇 (D)
    311.13,  // 夹钟 (D#)
    329.63,  // 姑洗 (E)
    349.23,  // 仲吕 (F)
    369.99,  // 蕤宾 (F#)
    392.00,  // 林钟 (G)
    415.30,  // 夷则 (G#)
    440.00,  // 南吕 (A)
    466.16,  // 无射 (A#)
    493.88   // 应钟 (B)
]

const lulu = [
    '黄钟', '大吕', '太簇', '夹钟', '姑洗', '仲吕',
    '蕤宾', '林钟', '夷则', '南吕', '无射', '应钟'
]

function playLulu(i) {
    const frequency = luluFrequencies[i]
    if (frequency) {
        // 使用不同的波形来区分音色
        const waveType = i % 3 === 0 ? 'sine' : i % 3 === 1 ? 'triangle' : 'sawtooth'
        playTone(frequency, 2.0, waveType, `lulu-${i}`)
    }
}

/* ---------------- 互动测验 ---------------- */
// 第2章-响应式对象
const bank = reactive([
    { q: '"十二律"中第一个律名？', ans: ['黄钟', '大吕', '太簇'], ok: '黄钟' },
    { q: '"角"对应唱名？', ans: ['Mi', 'Sol', 'La'], ok: 'Mi' },
    { q: '"羽"对应唱名？', ans: ['La', 'Do', 'Re'], ok: 'La' },
    { q: '"三分损益法"是谁提出的？', ans: ['管仲', '伶伦', '孔子'], ok: '伶伦' }
])

// 第2章-响应式数据
const cur = ref({})
const tip = ref('')

const next = () => {
    cur.value = bank[Math.floor(Math.random() * bank.length)]
}

next()

function check(a) {
    tip.value = a === cur.value.ok ? '✅ 正确' : '❌ 错误'
    setTimeout(() => (tip.value = ''), 1200)
}
</script>

<style scoped>
.theory-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.box {
    background: #2d2d2d;
    border-radius: 8px;
    padding: 20px;
}

.box h2 {
    color: #d4af37;
    margin-bottom: 12px;
}

.keys {
    margin-bottom: 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tone-play {
    padding: 8px 16px;
    border: 1px solid #d4af37;
    background: none;
    color: #d4af37;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
    min-width: 60px;
}

.tone-play:hover {
    background: #d4af37;
    color: #000;
}

.tone-play.playing {
    background: #d4af37;
    color: #000;
    transform: scale(0.95);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

.lulu {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 6px;
    text-align: center;
    font-size: 12px;
}

.lulu span {
    border: 1px solid #d4af37;
    border-radius: 4px;
    padding: 8px 4px;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 32px;
}

.lulu span:hover {
    background: #d4af37;
    color: #000;
}

.lulu span.playing {
    background: #d4af37;
    color: #000;
    transform: scale(0.95);
    box-shadow: 0 0 8px rgba(212, 175, 55, 0.4);
}

.quiz {
    display: flex;
    gap: 10px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.quiz button {
    padding: 8px 16px;
    border: 1px solid #d4af37;
    background: none;
    color: #d4af37;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
    flex: 1;
    min-width: 80px;
}

.quiz button:hover {
    background: #d4af37;
    color: #000;
}

.next {
    margin-top: 10px;
    padding: 8px 16px;
    border: 1px solid #d4af37;
    background: none;
    color: #d4af37;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}

.next:hover {
    background: #d4af37;
    color: #000;
}

.tip {
    margin-top: 8px;
    font-size: 13px;
    text-align: center;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.4s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.btn-collect {
    width: 100%;
    margin-top: 12px;
    padding: 8px 12px;
    border: 1px solid #d4af37;
    background: rgba(212, 175, 55, 0.1);
    color: #d4af37;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 14px;
}

.btn-collect:hover {
    background: #d4af37;
    color: #000;
}

.btn-collect.collected {
    background: #d4af37;
    color: #000;
    font-weight: bold;
}
</style>