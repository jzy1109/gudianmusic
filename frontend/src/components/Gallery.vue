<template>
    <section>
        <h2>作品长廊</h2>
        <div class="gall-bar">
            <select v-model="genre" @change="console.log('change事件', genre)">
                <option value="all">全部</option>
                <option value="guqin">古琴</option>
                <option value="pipa">琵琶</option>
            </select>
        </div>

        <!-- 计算属性筛选 -->
        <div class="waterfall">
            <div v-for="m in filteredMusic" :key="m.id" class="gcard">
                <img :src="`/image/${m.cover}`" />
                <div class="info">
                    <h3>{{ m.title }}</h3>
                    <p>{{ m.artist }} · {{ m.dynasty }}</p>
                    <div class="audio-controls">
                        <button @click="togglePlay(m)" :class="['play-btn', { playing: currentPlaying === m.id }]">
                            {{ getPlayButtonText(m) }}
                        </button>
                        <button @click="toggleCollect(m)" :class="['btn-collect', { collected: isCollected(m) }]">
                            {{ isCollected(m) ? '已收藏' : '加入收藏' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { addFavorite, delFavorite } from '../api/favorite.js'

/* ---------------- 数据 ---------------- */
const genre = ref('all')          // ✅ 只定义一次
const musicList = ref([])
const collectList = ref([])
const currentPlaying = ref(null)

/* ✅ 下拉监听（必打印） */
watch(genre, v => console.log('genre 变成', v))

/* ✅ 计算属性：下拉筛选 */
const filteredMusic = computed(() =>
    genre.value === 'all'
        ? musicList.value
        : musicList.value.filter(m => m.genre === genre.value)
)

/* ---------------- 音频 ---------------- */
let audioCtx = null
let playTimeouts = []
const noteFrequencies = {
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77
}

function getAudioContext() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    return audioCtx
}

/* ---------------- 生命周期 ---------------- */
onMounted(async () => {
  // 1. 全部作品
  const musicRes = await fetch('http://localhost:5000/api/music').then(r => r.json())
  musicList.value = musicRes.music

  // 2. 我的收藏（需登录）
  const favRes = await fetch('http://localhost:5000/api/favorites', {
    headers: { 'Authorization': `Bearer ${JSON.parse(localStorage.getItem('user') || '{}').id}` }
  }).then(r => r.json())
  if (favRes.success) {
    collectList.value = favRes.list          // ← 写入本地状态
  } else {
    collectList.value = []                   // 未登录或失败
  }
})

onUnmounted(() => {
    stopAllSounds()
})

/* ---------------- 播放 ---------------- */
function togglePlay(music) {
    if (currentPlaying.value === music.id) {
        stopAllSounds()
    } else {
        playMelody(music)
    }
}

function stopAllSounds() {
    playTimeouts.forEach(t => clearTimeout(t))
    playTimeouts = []
    currentPlaying.value = null
}

function playMelody(music) {
    stopAllSounds()
    currentPlaying.value = music.id
    const melody = generateMelody(music.title)
    const ctx = getAudioContext()
    let t = 0
    melody.forEach(({ note, duration }) => {
        const freq = noteFrequencies[note]
        playTimeouts.push(
            setTimeout(() => {
                if (currentPlaying.value !== music.id) return
                playNote(ctx, freq, duration, music.genre === 'pipa' ? 'square' : 'sine')
            }, t)
        )
        t += duration * 1000
    })
    playTimeouts.push(setTimeout(() => stopAllSounds(), t))
}

function playNote(ctx, freq, duration, type = 'sine') {
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.type = type
    osc.frequency.value = freq
    const now = ctx.currentTime
    gain.gain.setValueAtTime(0, now)
    gain.gain.linearRampToValueAtTime(0.3, now + 0.05)
    gain.gain.exponentialRampToValueAtTime(0.001, now + duration * 0.8)
    osc.connect(gain).connect(ctx.destination)
    osc.start(now)
    osc.stop(now + duration)
}

function generateMelody(title) {
    const map = {
        '高山流水': [
            { note: 'C4', duration: 0.8 }, { note: 'D4', duration: 0.6 }, { note: 'E4', duration: 1.2 },
            { note: 'G4', duration: 0.6 }, { note: 'A4', duration: 0.6 }, { note: 'G4', duration: 1.2 },
            { note: 'E4', duration: 0.6 }, { note: 'D4', duration: 0.6 }, { note: 'C4', duration: 2 }
        ],
        '十面埋伏': [
            { note: 'G3', duration: 0.4 }, { note: 'G3', duration: 0.4 }, { note: 'G3', duration: 0.4 },
            { note: 'C4', duration: 0.8 }, { note: 'D4', duration: 0.4 }, { note: 'E4', duration: 0.4 },
            { note: 'G4', duration: 1.2 }, { note: 'E4', duration: 0.4 }, { note: 'D4', duration: 0.8 }
        ],
        '春江花月夜': [
            { note: 'D4', duration: 1.0 }, { note: 'E4', duration: 0.5 }, { note: 'F4', duration: 0.5 },
            { note: 'G4', duration: 1.2 }, { note: 'E4', duration: 0.5 }, { note: 'D4', duration: 1.0 },
            { note: 'C4', duration: 0.5 }, { note: 'D4', duration: 2.0 }
        ]
    }
    return map[title] || map['高山流水']
}

function getPlayButtonText(music) {
    return currentPlaying.value === music.id ? '暂停' : '播放'
}

/* ---------------- 收藏 ---------------- */
function toggleCollect(music) {
    const item = {
        type: 'work',
        key: `work-${music.id}`,
        name: music.title,
        icon: '🎵',
        brief: `${music.artist} · ${music.dynasty}`
    }
    const collected = isCollected(music)
    if (collected) {
        delFavorite(item).then(() => {
            collectList.value = collectList.value.filter(i => i.key !== item.key)
        })
    } else {
        addFavorite(item).then(() => {
            collectList.value.push(item)
        })
    }
}

function isCollected(music) {
    return collectList.value.some(i => i.key === `work-${music.id}`)
}
</script>

<style scoped>
.gall-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px
}

.gall-bar h2 {
    color: #d4af37
}

.gall-bar select {
    margin-left: auto;
    background: #2d2d2d;
    border: 1px solid #d4af37;
    color: #eee;
    padding: 4px 8px;
    border-radius: 4px;
    outline: none
}

.waterfall {
    column-count: 4;
    column-gap: 16px
}

.gcard {
    background: #2d2d2d;
    border-radius: 8px;
    overflow: hidden;
    break-inside: avoid;
    margin-bottom: 16px
}

.gcard img {
    width: 100%;
    display: block;
    cursor: pointer
}

.gcard .info {
    padding: 12px
}

.gcard h3 {
    color: #d4af37;
    margin-bottom: 4px;
    font-size: 16px
}

.gcard p {
    font-size: 13px;
    color: #ccc;
    margin-bottom: 12px
}

.audio-controls {
    display: flex;
    gap: 8px
}

.play-btn,
.btn-collect {
    padding: 0 12px;
    border: 1px solid #d4af37;
    background: none;
    color: #d4af37;
    border-radius: 4px;
    cursor: pointer;
    transition: all .3s;
    flex: 1;
    font-size: 12px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1
}

.play-btn:hover,
.btn-collect:hover {
    background: #d4af37;
    color: #000
}

.play-btn.playing,
.btn-collect.collected {
    background: #d4af37;
    color: #000
}

@media (max-width:768px) {
    .waterfall {
        column-count: 2
    }

    .audio-controls {
        flex-direction: column
    }
}

@media (max-width:480px) {
    .waterfall {
        column-count: 1
    }
}
</style>