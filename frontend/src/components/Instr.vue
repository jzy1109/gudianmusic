<template>
  <section class="instr-page">

    <!-- =============== 内容区 =============== -->
    <main class="instr-content">
      <!-- 网格视图 -->
      <template v-if="mode !== 'play'">
        <div class="grid-top-bar">
          <button @click="mode = 'grid'" :class="{ active: mode === 'grid' }">网格视图</button>
          <button @click="mode = 'play'" :class="{ active: mode === 'play' }">演奏厅</button>
        </div>
        <div class="grid">
          <div v-for="ins in list" :key="ins.id" class="card" @click="toPlay(ins)">
            <div class="icon">{{ ins.icon }}</div>
            <h3>{{ ins.name }}</h3>
            <p>{{ ins.brief }}</p>
            <button @click.stop="toggle(ins)" :class="{ collected: ins.collected }">
              {{ ins.collected ? '已收藏' : '收藏' }}
            </button>
          </div>
        </div>
      </template>

      <!-- 演奏厅视图 -->
      <template v-else>
        <div class="play-top-bar">
          <button @click="mode = 'grid'" :class="{ active: mode === 'grid' }">网格视图</button>
          <button @click="mode = 'play'" :class="{ active: mode === 'play' }">演奏厅</button>
        </div>
        <div class="play-hall">
          <!-- 乐谱独立卡片 -->
          <div class="score-display" v-if="currentIns?.score">
            <div class="score-header">
              <h3>📜 {{ currentIns.score.name }}</h3>
              <span class="instrument-type">{{ currentIns.name }}专用谱</span>
            </div>
            <div class="score-main">
              <div class="score-notation">
                <div v-for="(line, idx) in currentIns.score.notation" :key="idx" class="score-line">
                  <span class="line-number">{{ idx + 1 }}</span>
                  <span class="line-content">{{ line }}</span>
                </div>
              </div>
              <div class="score-legend">
                <h4>📖 曲谱说明</h4>
                <p>{{ currentIns.score.guide }}</p>
                <div class="note-mapping" v-if="currentIns.score.mapping">
                  <h5>🎵 音高对照</h5>
                  <div class="mapping-grid">
                    <div v-for="(desc, note) in currentIns.score.mapping" :key="note" class="mapping-item">
                      <span class="note">{{ note }}</span>
                      <span class="desc">{{ desc }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 大乐器本体 -->
          <div class="instrument-display">
            <!-- 古琴 -->
            <div v-if="currentIns?.id === 1" class="guqin">
              <div class="guqin-body">
                <div v-for="(s, i) in currentIns.keys" :key="i" class="guqin-string" @click="playString(i)"
                  :class="{ playing: playingIdx === i }">
                  <div class="string-line" />
                  <div v-for="f in [3, 6, 8, 10]" :key="f" class="fret-marker" :style="{ left: f * 8 + '%' }" />
                </div>
              </div>
            </div>

            <!-- 琵琶 -->
            <div v-else-if="currentIns?.id === 2" class="pipa-playground">
              <div class="pipa-container">
                <div class="pipa-instrument">
                  <div class="pipa-head">
                    <div class="tuning-pegs">
                      <div v-for="n in 4" :key="n" class="tuning-peg" />
                    </div>
                  </div>
                  <div class="pipa-neck">
                    <div class="frets">
                      <div v-for="f in 6" :key="f" class="fret" />
                    </div>
                  </div>
                  <div class="pipa-body">
                    <div class="sound-holes">
                      <div class="sound-hole left" />
                      <div class="sound-hole right" />
                    </div>
                    <div class="pipa-strings">
                      <div v-for="(s, i) in currentIns.keys" :key="i" class="pipa-string" @click="playString(i)"
                        :class="{ playing: playingIdx === i }">
                        <div class="string-line" />
                        <div class="pluck-effect" v-if="playingIdx === i" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <p class="hint">点击琴弦进行弹奏，从细到粗分别为子弦、中弦、老弦、缠弦</p>
            </div>

            <!-- 二胡 -->
            <div v-else-if="currentIns?.id === 3" class="erhu">
              <div class="erhu-body">
                <div class="erhu-neck" />
                <div class="erhu-strings">
                  <div v-for="(s, i) in currentIns.keys" :key="i" class="erhu-string" @click="playString(i)"
                    :class="{ playing: playingIdx === i }">
                    <div class="string-line" />
                  </div>
                </div>
                <div class="erhu-resonator" />
                <div class="erhu-bow" />
              </div>
            </div>

            <!-- 笛子 -->
            <div v-else-if="currentIns?.id === 4" class="dizi-playground">
              <div class="dizi-container">
                <div class="dizi-instrument">
                  <div class="dizi-tube">
                    <!-- 吹口 -->
                    <div class="blow-hole" @click="playString(0)" />
                    <div class="membrane-hole">
                      <div class="dizi-membrane" />
                    </div>
                    <!-- 音孔 1-5 -->
                    <div v-for="i in 5" :key="i" class="dizi-hole" @click="playString(i)"
                      :class="{ playing: playingIdx === i }" :style="{ left: (20 + (i - 1) * 12) + '%' }">
                      <div class="hole-ring" />
                      <div class="finger-cover" v-if="holeCovered[i - 1]" />
                    </div>
                    <div class="base-holes">
                      <div v-for="n in 2" :key="n" class="base-hole" />
                    </div>
                  </div>
                </div>
                <!-- 指法按钮 -->
                <div class="fingering-chart">
                  <button v-for="i in 5" :key="i" class="finger-indicator" :class="{ active: holeCovered[i - 1] }"
                    @click="toggleFinger(i - 1)">
                    {{ i }}
                  </button>
                </div>
              </div>
              <p class="hint">🎵 点击音孔进行演奏，可点击下方数字模拟手指按孔</p>
            </div>

            <!-- 古筝 -->
            <div v-else-if="currentIns?.id === 5" class="guzheng">
              <div class="guzheng-body">
                <div v-for="(s, i) in currentIns.keys" :key="i" class="guzheng-string" @click="playString(i)"
                  :class="{ playing: playingIdx === i }">
                  <div class="string-line" />
                  <div class="bridge" />
                </div>
              </div>
            </div>

            <!-- 编钟 -->
            <div v-else-if="currentIns?.id === 6" class="bianzhong">
              <div class="bianzhong-body">
                <div v-for="(b, i) in currentIns.keys" :key="i" class="bianzhong-bell" @click="playString(i)"
                  :class="{ playing: playingIdx === i }">
                  <div class="bell" />
                  <div class="bell-handle" />
                </div>
              </div>
            </div>

            <!-- 唢呐 -->
            <div v-else-if="currentIns?.id === 7" class="suona-playground">
              <div class="suona-container">
                <div class="suona-instrument">
                  <div class="reed" @click="playString(0)">
                    <div class="reed-tip" />
                  </div>
                  <div class="suona-core" />
                  <div class="suona-body">
                    <div v-for="i in 7" :key="i" class="suona-hole" @click="playString(i)"
                      :class="{ playing: playingIdx === i }" :style="{ left: (15 + (i - 1) * 16) + '%' }">
                      <div class="hole-indicator" />
                      <div class="breath-effect" v-if="playingIdx === i" />
                    </div>
                  </div>
                  <div class="suona-bell">
                    <div class="bell-flare" />
                  </div>
                </div>

              </div>
              <p class="hint">点击哨片和音孔进行演奏，模拟吹奏气息</p>
            </div>

            <!-- 箫 -->
            <div v-else-if="currentIns?.id === 8" class="xiao-playground">
              <div class="xiao-container">
                <div class="xiao-instrument">
                  <div class="xiao-tube">
                    <div class="xiao-mouthpiece" @click="playString(0)">
                      <div class="mouth-cut" />
                    </div>
                    <div v-for="i in 5" :key="i" class="xiao-hole" @click="playString(i)"
                      :class="{ playing: playingIdx === i }" :style="{ left: (25 + (i - 1) * 14) + '%' }">
                      <div class="hole-outline" />
                      <div class="xiao-finger-cover" v-if="xiaoHoleCovered[i - 1]" />
                    </div>
                  </div>
                </div>
                <div class="xiao-fingering">
                  <button v-for="i in 5" :key="i" class="xiao-finger-btn" :class="{ covered: xiaoHoleCovered[i - 1] }"
                    @click="toggleXiaoFinger(i - 1)">
                    <span class="finger-number">{{ i }}</span>
                    <span class="finger-name">{{ getXiaoFingerName(i - 1) }}</span>
                  </button>
                </div>
              </div>
              <p class="hint">点击吹口和音孔进行演奏，可切换指法模拟不同音高</p>
            </div>

            <!-- 默认键盘 -->
            <div v-else class="keys">
              <button v-for="(note, i) in currentIns.keys" :key="i" @click="playString(i)"
                :class="{ on: playingIdx === i }">
                {{ note }} <!-- 按钮文字 -->
              </button>
            </div>

            <!-- 当前音高+音色 -->
            <div class="current-meta">
              <span>当前音高：{{ currentNote || '—' }}</span>
              <span>音色：{{ currentIns?.toneType }}</span>
            </div>

            <!-- 返回乐器列表 -->
            <div style="margin-top: 12px; text-align: center;">
              <button class="back-btn" @click="mode = 'grid'">返回乐器列表</button>
            </div>

            <!-- 底部提示 -->
            <p class="hint">点击{{ getInstrumentPartName() }}聆听音色</p>
          </div>
        </div>
      </template>
    </main>
  </section>
</template>

<script setup>
/* ------------------ 引入 & 注入 ------------------ */
import { ref, reactive, onMounted, onActivated } from 'vue'
import { addFavorite, delFavorite, getFavorites } from '../api/favorite.js'

const emit = defineEmits(['update:collectList'])
const props = defineProps({ collectList: Array })

/* -------- 主导航用常量 & 函数 -------- */
const tabs = [
  { id: 'origin', name: '音乐起源' },
  { id: 'instr', name: '传统乐器' },
  { id: 'theory', name: '音乐理论' },
  { id: 'gallery', name: '作品长廊' },
  { id: 'collect', name: '我的收藏' }
]
const currentTab = ref('instr')   // 默认当前页就是乐器页

function switchTab(tabId) {
  currentTab.value = tabId
  // 如果你想切路由，再自行加 router.push
}

function getTabIcon(tabId) {
  const map = { origin: '🎵', instr: '🎻', theory: '📚', gallery: '🖼️', collect: '❤️' }
  return map[tabId] || '📄'
}
/* ------------------------------------ */

/* ------------------ 音频 ------------------ */
let audioContext = null
let currentOscillator = null
const noteFrequencies = {
  C2: 65.41, D2: 73.42, E2: 82.41, F2: 87.31, G2: 98.00, A2: 110.00, B2: 123.47,
  C3: 130.81, D3: 146.83, E3: 164.81, F3: 174.61, G3: 196.00, A3: 220.00, B3: 246.94,
  C4: 261.63, D4: 293.66, E4: 329.63, F4: 349.23, G4: 392.00, A4: 440.00, B4: 493.88,
  C5: 523.25, D5: 587.33, E5: 659.25, F5: 698.46, G5: 783.99, A5: 880.00, B5: 987.77,
  C6: 1046.50, D6: 1174.66, E6: 1318.51, F6: 1396.91, G6: 1567.98, A6: 1760.00
}

function initAudio() {
  if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)()
}

function playTone(freq, duration = 1, type = 'sine') {
  initAudio()
  if (currentOscillator) currentOscillator.stop()
  const osc = audioContext.createOscillator()
  const gain = audioContext.createGain()
  osc.type = type
  osc.frequency.setValueAtTime(freq, audioContext.currentTime)
  gain.gain.setValueAtTime(0, audioContext.currentTime)
  gain.gain.linearRampToValueAtTime(0.3, audioContext.currentTime + 0.05)
  gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration * 0.8)
  osc.connect(gain).connect(audioContext.destination)
  osc.start()
  osc.stop(audioContext.currentTime + duration)
  currentOscillator = osc
}

/* ------------------ 状态 ------------------ */
const mode = ref('grid')
const playingIdx = ref(null)
const currentNote = ref('')
const currentIns = ref(null)
const fingerPosition = ref(0)
const holeCovered = ref([false, false, false, false, false, false])
const xiaoHoleCovered = ref([false, false, false, false, false])
const isBlowing = ref(false)

/* ------------------ 乐器数据（含曲谱） ------------------ */
const list = reactive([
  {
    id: 1, name: '古琴', icon: '🎻', brief: '七弦，文人雅士之器', collected: false,
    keys: Array.from({ length: 7 }, (_, i) => i), toneType: '深沉悠远',
    scale: ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3'],
    score: {
      name: '古琴《梅花三弄》片段',
      notation: ['⿰丿四  ⿰亻心  ⿰扌乚  ⿰口刀', '⿰女子  ⿰日辰  ⿰木子  ⿰金戋', '⿰水工  ⿰火乍  ⿰土也  ⿰石开', '泛音起  散音承  按音转  撮音合'],
      guide: '古琴减字谱：每个组合字表示指法（左）和位置（右）',
      mapping: { C3: '一弦散音', D3: '二弦散音', E3: '三弦散音', F3: '四弦散音', G3: '五弦散音', A3: '六弦散音', B3: '七弦散音' }
    }
  },
  {
    id: 2, name: '琵琶', icon: '🪕', brief: '四弦曲项，弹拨之王', collected: false,
    keys: Array.from({ length: 4 }, (_, i) => i), toneType: '清脆明亮',
    scale: ['G3', 'A3', 'B3', 'C4'],
    score: {
      name: '琵琶《阳春白雪》简谱',
      notation: ['6   -   2   -   |   3   -   5   -   |', '6   1   2   3   |   2   -   -   -   |', '3   5   6   1   |   5   -   -   -   |', '2   3   5   6   |   1   6   5   3   |', '2   3   2   1   |   6   1   2   -   |'],
      guide: '四弦定音：A(子弦) D(中弦) E(老弦) A(缠弦)',
      mapping: { G3: '缠弦空弦', A3: '老弦空弦', B3: '中弦第2品', C4: '子弦空弦' }
    }
  },
  {
    id: 3, name: '二胡', icon: '🎻', brief: '二弦拉奏，如歌如泣', collected: false,
    keys: Array.from({ length: 2 }, (_, i) => i), toneType: '婉转悠扬',
    scale: ['D4', 'A4'],
    score: {
      name: '二胡《二泉映月》片段',
      notation: ['6   5   3   5   |   6   -   -   -   |', '1   6   5   3   |   2   -   -   -   |', '3   5   6   1   |   5   3   2   1   |', '6   1   2   3   |   5   -   6   -   |', '1   6   5   3   |   2   3   1   6   |'],
      guide: '内弦定D，外弦定A，使用传统把位',
      mapping: { D4: '内弦空弦', A4: '外弦空弦' }
    }
  },
  {
    id: 4, name: '笛子', icon: '🎵', brief: '横吹竹制，清脆悠远', collected: false,
    keys: Array.from({ length: 6 }, (_, i) => i), toneType: '清脆悠扬',
    scale: ['D5', 'E5', 'F5', 'G5', 'A5', 'B5'],
    score: {
      name: '笛子《姑苏行》片段',
      notation: ['5   6   1   2   |   3   2   1   6   |', '5   -   6   1   |   2   3   2   -   |', '3   5   6   1   |   5   6   5   3   |', '2   3   2   1   |   6   1   2   -   |', '3   5   6   1   |   2   3   5   6   |'],
      guide: '筒音作5，G调指法，注意气息控制',
      mapping: { D5: '全按作5', E5: '开一孔', F5: '开二孔', G5: '开三孔', A5: '开四孔', B5: '开五孔' }
    }
  },
  {
    id: 5, name: '古筝', icon: '🎼', brief: '二十一弦，华丽典雅', collected: false,
    keys: Array.from({ length: 21 }, (_, i) => i), toneType: '华丽典雅',
    scale: ['G2', 'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5'],
    score: {
      name: '古筝《渔舟唱晚》简谱',
      notation: ['3   5   6   2   3   |   5   6   1   2   3   |', '5   6   1   2   3   |   5   6   1   2   3   |', '6   1   2   3   5   |   3   2   1   6   5   |', '3   2   1   6   5   |   3   2   1   -   -   |', '......'],
      guide: 'D调定弦，绿弦为5(sol)，右手托劈勾剔，左手按滑',
      mapping: { G2: '最低音弦', C4: '中音区', F5: '最高音弦' }
    }
  },
  {
    id: 6, name: '编钟', icon: '🔔', brief: '青铜打击，礼乐重器', collected: false,
    keys: Array.from({ length: 8 }, (_, i) => i), toneType: '浑厚庄严',
    scale: ['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4'],
    score: {
      name: '编钟《楚商》片段',
      notation: ['1   -   2   -   |   3   -   5   -   |', '6   -   5   -   |   3   -   2   -   |', '1   2   3   5   |   6   5   3   2   |', '1   -   -   -   |   //   钟鸣   //   |', '1   3   5   6   |   5   3   2   1   |'],
      guide: '双音钟，一钟两音，敲击正中与侧面音高不同',
      mapping: { C3: '黄钟', D3: '太簇', E3: '姑洗', F3: '仲吕', G3: '林钟', A3: '南吕', B3: '应钟', C4: '清黄钟' }
    }
  },
  {
    id: 7, name: '唢呐', icon: '🎺', brief: '高亢嘹亮，民间必备', collected: false,
    keys: Array.from({ length: 7 }, (_, i) => i), toneType: '高亢嘹亮',
    scale: ['G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5'],
    score: {
      name: '唢呐《百鸟朝凤》片段',
      notation: ['5   -   6   -   |   5   3   2   1   |', '6   5   3   5   |   6   -   -   -   |', '1   6   5   3   |   2   -   3   -   |', '5   6   1   2   |   3   2   1   6   |', '5   -   -   -   |   ~~   鸟鸣   ~~   |'],
      guide: 'D调唢呐，筒音作5，注意循环换气',
      mapping: { G4: '筒音5', A4: '开一孔6', C5: '开三孔1', D5: '开四孔2', E5: '开五孔3', G5: '超吹5', A5: '超吹6' }
    }
  },
  {
    id: 8, name: '箫', icon: '🎶', brief: '竖吹音色，幽静淡雅', collected: false,
    keys: Array.from({ length: 6 }, (_, i) => i), toneType: '幽静淡雅',
    scale: ['D4', 'F4', 'G4', 'A4', 'C5'],
    score: {
      name: '箫《梅花三弄》片段',
      notation: ['1   -   2   -   |   3   -   5   -   |', '6   -   5   3   |   2   -   -   -   |', '5   6   1   2   |   3   2   1   6   |', '5   -   6   1   |   2   3   5   6   |', '1   6   5   3   |   2   3   1   6   |'],
      guide: 'G调箫，筒音作5，口风要松，气息要缓',
      mapping: { D4: '筒音5', F4: '开一二孔7', G4: '开二三孔1', A4: '开三四孔2', C5: '开五六孔4' }
    }
  }
])

/* ------------------ 业务函数 ------------------ */
function toPlay(ins) {
  currentIns.value = ins
  mode.value = 'play'
  initAudio()
  holeCovered.value = [false, false, false, false, false, false]
  xiaoHoleCovered.value = [false, false, false, false, false]
  isBlowing.value = false
}

function insKeyName(i) {
  return `音${i + 1}`
}

function getInstrumentPartName() {
  if (!currentIns.value) return '琴弦'
  const id = currentIns.value.id
  if ([1, 2, 3, 5].includes(id)) return '琴弦'
  if ([4, 8].includes(id)) return '音孔'
  if (id === 6) return '钟体'
  if (id === 7) return '音孔'
  return '按键'
}

function toggleFinger(i) {
  holeCovered.value[i] = !holeCovered.value[i]
}
function toggleXiaoFinger(i) {
  xiaoHoleCovered.value[i] = !xiaoHoleCovered.value[i]
}
function getXiaoFingerName(i) {
  return ['食指', '中指', '无名指', '小指', '拇指'][i] || '手指'
}

function startBlowing() {
  isBlowing.value = true
}
function stopBlowing() {
  isBlowing.value = false
}

function playString(i) {
  const ins = currentIns.value
  if (!ins || !ins.scale) {
    console.error('乐器数据错误', ins)
    return
  }

  // 箫特殊处理：吹口(i=0)不发声，音孔 1-5 对应 scale 0-4
  if (ins.id === 8) {
    if (i === 0) {
      // 吹口不发声
      playingIdx.value = null
      return
    }
    const scaleIndex = i - 1
    if (scaleIndex < 0 || scaleIndex >= ins.scale.length) {
      console.error('箫孔索引越界', i, 'scale长度', ins.scale.length)
      playingIdx.value = null
      return
    }
    const note = ins.scale[scaleIndex]
    const freq = noteFrequencies[note]
    if (!freq) {
      console.error('频率未找到', note)
      playingIdx.value = null
      return
    }
    currentNote.value = note
    playingIdx.value = i
    playTone(freq, 1.2, 'sine')
    return
  }

  // 其他乐器处理
  const freq = noteFrequencies[ins.scale[i]]
  if (!freq) {
    console.error('频率未找到', ins.scale[i])
    playingIdx.value = null
    return
  }
  currentNote.value = ins.scale[i]
  playingIdx.value = i
  playTone(freq, 1.2, 'sine')
}

async function syncCollectedStatus() {
  const res = await getFavorites()
  if (!res.success) return
  const collectedKeys = new Set(res.list.map(x => x.key))
  list.forEach(ins => {
    ins.collected = collectedKeys.has(`instr-${ins.id}`)
  })
  const newList = list.filter(ins => ins.collected).map(ins => ({
    ...ins,
    type: 'instr',
    key: `instr-${ins.id}`,
    name: ins.name,
    icon: ins.icon,
    brief: ins.brief
  }))
  emit('update:collectList', newList)
}

async function toggle(ins) {
  const key = `instr-${ins.id}`
  const item = {
    type: 'instr',
    key,
    name: ins.name,
    icon: ins.icon,
    brief: ins.brief
  }

  // 1. 先和后端通信（等待成功）
  const res = ins.collected
    ? await delFavorite(item)
    : await addFavorite(item)

  if (!res.success) {
    alert(res.message || '操作失败')
    return            // 失败就退出，不改变状态
  }

  // 2. 成功了再改本地 + 通知父组件重新拉库
  ins.collected = !ins.collected
  emit('update:collectList')   // 触发 App.vue 的 syncCollect()
}

/* ------------------ 生命周期 ------------------ */
onMounted(async () => {
  await syncCollectedStatus()
})
onActivated(async () => {
  await syncCollectedStatus()
})
</script>

<style scoped>
/* =============== 基础布局 =============== */
.instr-page {
  min-height: 100vh;
  background: #1a1a1a;
  color: #eee;
  font-family: STKaiti, KaiTi, serif;
  padding: 20px
}

.instr-sticky-head {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #1a1a1a;
  border-bottom: 2px solid #d4af37;
  padding-bottom: 12px
}

.main-nav {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px
}

.main-nav button {
  padding: 8px 16px;
  border: 1px solid #d4af37;
  background: none;
  color: #d4af37;
  border-radius: 4px;
  cursor: pointer;
  transition: all .3s
}

.main-nav button.active {
  background: #d4af37;
  color: #000;
  font-weight: bold
}

.mode-bar {
  display: flex;
  justify-content: center;
  gap: 12px
}

.mode-bar button {
  padding: 6px 14px;
  border: 1px solid #d4af37;
  background: none;
  color: #d4af37;
  border-radius: 4px;
  cursor: pointer;
  transition: all .3s
}

.mode-bar button.active {
  background: #d4af37;
  color: #000
}

/* =============== 网格 =============== */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px
}

.card {
  background: #2d2d2d;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: transform .3s
}

.card:hover {
  transform: translateY(-4px)
}

.card .icon {
  font-size: 40px;
  margin-bottom: 8px
}

.card h3 {
  color: #d4af37;
  margin-bottom: 4px
}

.card p {
  font-size: 13px;
  color: #ccc;
  margin-bottom: 10px
}

.card button {
  width: 100%;
  padding: 6px;
  border: 1px solid #d4af37;
  background: none;
  color: #d4af37;
  border-radius: 4px;
  cursor: pointer;
  transition: all .3s
}

.card button.collected,
.card button:hover {
  background: #d4af37;
  color: #000
}

/* =============== 演奏厅 =============== */
.play-hall {
  background: #2d2d2d;
  border: 1px solid #444;
  border-radius: 12px;
  padding: 24px 20px 20px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, .5)
}

.play-hall h2 {
  color: #d4af37;
  margin-bottom: 16px
}

.current-meta {
  margin: 16px 0 8px;
  font-size: 16px;
  color: #ccc;
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap
}

.current-meta span:first-child {
  color: #d4af37;
  font-weight: bold
}

.hint {
  margin: 0 0 12px;
  font-size: 14px;
  color: #aaa
}

.back-btn {
  margin-top: 12px;
  padding: 8px 16px;
  border: 1px solid #d4af37;
  background: none;
  color: #d4af37;
  border-radius: 4px;
  cursor: pointer;
  transition: all .3s;
  font-size: 14px
}

.back-btn:hover {
  background: #d4af37;
  color: #000
}

/* =============== 谱面卡片 =============== */
.score-display {
  background: linear-gradient(135deg, rgba(40, 40, 40, .95), rgba(30, 30, 30, .98));
  border: 2px solid #d4af37;
  border-radius: 16px;
  padding: 25px;
  margin: 25px auto 35px;
  max-width: 900px;
  box-shadow: 0 10px 30px rgba(212, 175, 55, .25);
  backdrop-filter: blur(10px)
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(212, 175, 55, .3)
}

.score-header h3 {
  color: #d4af37;
  font-size: 22px;
  margin: 0;
  font-weight: bold
}

.instrument-type {
  background: rgba(212, 175, 55, .15);
  color: #ffd700;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  border: 1px solid rgba(212, 175, 55, .3)
}

.score-main {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 25px
}

.score-notation {
  flex: 2;
  min-width: 500px;
  background: rgba(10, 10, 10, .7);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(212, 175, 55, .2);
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, .5)
}

.score-line {
  display: flex;
  align-items: center;
  margin: 12px 0;
  font-family: 'Noto Serif SC', 'STKaiti', serif;
  font-size: 20px;
  line-height: 1.8;
  min-height: 36px
}

.line-number {
  color: #888;
  width: 30px;
  text-align: right;
  margin-right: 15px;
  font-size: 14px;
  opacity: .7
}

.line-content {
  flex: 1;
  color: #f0f0f0;
  letter-spacing: 8px;
  text-align: center;
  font-weight: 500
}

.score-legend {
  flex: 1;
  min-width: 300px;
  padding: 20px;
  background: rgba(212, 175, 55, .08);
  border-radius: 12px;
  border-left: 4px solid #d4af37
}

.score-legend h4 {
  color: #d4af37;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px
}

.score-legend p {
  color: #ccc;
  line-height: 1.7;
  margin-bottom: 20px;
  font-size: 15px
}

.note-mapping {
  margin-top: 20px
}

.note-mapping h5 {
  color: #ffd700;
  margin-bottom: 10px;
  font-size: 16px
}

.mapping-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px
}

.mapping-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(255, 255, 255, .05);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, .1)
}

.mapping-item .note {
  color: #d4af37;
  font-weight: bold;
  font-family: 'Courier New', monospace
}

.mapping-item .desc {
  color: #aaa;
  font-size: 13px;
  text-align: right
}

/* =============== 乐器本体 =============== */
.instrument-display {
  margin: 30px 0;
  min-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center
}

/* 古琴 */
.guqin {
  width: 500px;
  height: 100px;
  position: relative;
  margin: 0 auto
}

.guqin-body {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #5D4037, #6D4C41);
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, .4);
  display: flex;
  justify-content: space-between;
  padding: 0 15px
}

.guqin-string {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background .3s;
  margin: 0 3px
}

.guqin-string:hover {
  background: rgba(212, 175, 55, .1)
}

.guqin-string.playing {
  background: rgba(212, 175, 55, .2)
}

.guqin-string .string-line {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #e0e0e0, transparent)
}

.fret-marker {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 20px;
  background: #d4af37;
  border-radius: 2px
}

/* 琵琶 */
.pipa-playground {
  text-align: center
}

.pipa-container {
  position: relative;
  height: 320px;
  display: flex;
  justify-content: center;
  align-items: center
}

.pipa-instrument {
  width: 250px;
  height: 300px;
  position: relative
}

.pipa-head {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 40px;
  background: linear-gradient(45deg, #8B4513, #A0522D);
  border-radius: 8px 8px 0 0
}

.tuning-pegs {
  display: flex;
  justify-content: space-around;
  padding: 5px
}

.tuning-peg {
  width: 8px;
  height: 12px;
  background: #5D4037;
  border-radius: 4px
}

.pipa-neck {
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 80px;
  background: linear-gradient(45deg, #5D4037, #6D4C41);
  border-radius: 4px
}

.frets {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%
}

.fret {
  position: absolute;
  left: 0;
  width: 100%;
  height: 1px;
  background: #d4af37;
  opacity: .6
}

.fret:nth-child(1) {
  top: 20%
}

.fret:nth-child(2) {
  top: 35%
}

.fret:nth-child(3) {
  top: 50%
}

.fret:nth-child(4) {
  top: 65%
}

.fret:nth-child(5) {
  top: 80%
}

.fret:nth-child(6) {
  top: 95%
}

.pipa-body {
  position: absolute;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 160px;
  background: linear-gradient(135deg, #8B4513, #CD853F);
  border-radius: 50% 50% 60% 60%;
  box-shadow: 0 10px 20px rgba(0, 0, 0, .3)
}

.sound-holes {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  display: flex;
  justify-content: space-between
}

.sound-hole {
  width: 20px;
  height: 30px;
  background: #000;
  border-radius: 40%;
  opacity: .6
}

.pipa-strings {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 30px 0
}

.pipa-string {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all .3s
}

.pipa-string:hover {
  background: rgba(212, 175, 55, .1)
}

.pipa-string.playing {
  background: rgba(212, 175, 55, .2)
}

.pipa-string .string-line {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #fff, transparent)
}

.pluck-effect {
  position: absolute;
  left: 50%;
  width: 8px;
  height: 8px;
  background: #d4af37;
  border-radius: 50%;
  animation: pluckWave .6s ease-out
}

@keyframes pluckWave {
  0% {
    transform: scale(0);
    opacity: 1
  }

  100% {
    transform: scale(3);
    opacity: 0
  }
}

/* 二胡 */
.erhu {
  width: 200px;
  height: 300px;
  position: relative;
  margin: 0 auto
}

.erhu-body {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center
}

.erhu-neck {
  position: absolute;
  top: 0;
  width: 8px;
  height: 180px;
  background: linear-gradient(45deg, #8B4513, #A0522D);
  border-radius: 4px
}

.erhu-strings {
  position: absolute;
  top: 20px;
  width: 60px;
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: space-between
}

.erhu-string {
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all .3s;
  padding: 10px 0
}

.erhu-string:hover {
  background: rgba(212, 175, 55, .1)
}

.erhu-string.playing {
  background: rgba(212, 175, 55, .2)
}

.erhu-string .string-line {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #fff, transparent)
}

.erhu-resonator {
  position: absolute;
  bottom: 40px;
  width: 80px;
  height: 60px;
  background: linear-gradient(45deg, #8B4513, #A0522D);
  border-radius: 50%;
  border: 3px solid #5D4037
}

.erhu-bow {
  position: absolute;
  right: -40px;
  top: 80px;
  width: 120px;
  height: 2px;
  background: #8B4513;
  transform: rotate(15deg)
}

/* 古筝 */
.guzheng {
  width: 600px;
  height: 120px;
  position: relative;
  margin: 0 auto
}

.guzheng-body {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #8B4513, #A0522D);
  border-radius: 10px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, .5);
  display: flex;
  justify-content: space-between;
  padding: 0 20px
}

.guzheng-string {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all .3s;
  margin: 0 2px;
  position: relative
}

.guzheng-string:hover {
  background: rgba(212, 175, 55, .1)
}

.guzheng-string.playing {
  background: rgba(212, 175, 55, .2)
}

.guzheng-string .string-line {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #ddd, transparent)
}

.bridge {
  position: absolute;
  right: 10%;
  width: 4px;
  height: 100%;
  background: #d4af37;
  border-radius: 2px
}

/* 编钟 */
.bianzhong {
  width: 500px;
  height: 200px;
  position: relative;
  margin: 0 auto
}

.bianzhong-body {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  padding-top: 20px
}

.bianzhong-bell {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform .3s;
  padding: 10px
}

.bianzhong-bell:hover {
  transform: translateY(-5px)
}

.bianzhong-bell.playing {
  transform: translateY(-10px);
  animation: bellRing .5s ease-in-out
}

@keyframes bellRing {

  0%,
  100% {
    transform: translateY(-10px) rotate(0)
  }

  25% {
    transform: translateY(-10px) rotate(5deg)
  }

  75% {
    transform: translateY(-10px) rotate(-5deg)
  }
}

.bianzhong-bell .bell {
  width: 40px;
  height: 50px;
  background: linear-gradient(45deg, #B8860B, #DAA520);
  border-radius: 50% 50% 40% 40%;
  border: 3px solid #8B4513;
  box-shadow: 0 4px 8px rgba(0, 0, 0, .3)
}

.bianzhong-bell .bell-handle {
  width: 10px;
  height: 15px;
  background: #8B4513;
  border-radius: 5px 5px 0 0
}

/* 笛子音孔样式已在上文包含 */

/* 唢呐音孔样式已在上文包含 */

/* 箫音孔样式已在上文包含 */

/* 默认键盘 */
.keys {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 400px
}

.keys button {
  padding: 12px 16px;
  border: 1px solid #d4af37;
  background: rgba(212, 175, 55, .1);
  color: #d4af37;
  border-radius: 6px;
  cursor: pointer;
  transition: all .3s;
  min-width: 60px
}

.keys button:hover {
  background: rgba(212, 175, 55, .2)
}

.keys button.on {
  background: #d4af37;
  color: #000;
  transform: scale(.95)
}

/* ---- 笛子 ---- */
.dizi-playground {
  text-align: center
}

.dizi-container {
  position: relative;
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center
}

.dizi-tube {
  position: relative;
  width: 350px;
  height: 60px;
  background: linear-gradient(45deg, #90EE90, #32CD32);
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, .2)
}

.blow-hole {
  position: absolute;
  left: 8%;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 8px;
  background: #8B4513;
  border-radius: 4px;
  cursor: pointer
}

.membrane-hole {
  position: absolute;
  left: 15%;
  top: 50%;
  transform: translateY(-50%);
  width: 10px;
  height: 10px;
  background: #FFD700;
  border-radius: 50%;
  border: 1px solid #8B4513
}

.dizi-membrane {
  width: 100%;
  height: 100%;
  background: rgba(255, 215, 0, .6);
  border-radius: 50%;
  animation: membraneVibrate .3s ease-in-out
}

@keyframes membraneVibrate {

  0%,
  100% {
    transform: scale(1)
  }

  50% {
    transform: scale(1.2)
  }
}

.dizi-hole {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 30px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all .3s
}

.dizi-hole:hover {
  background: rgba(212, 175, 55, .1)
}

.dizi-hole.playing {
  background: rgba(212, 175, 55, .2)
}

.hole-ring {
  width: 16px;
  height: 16px;
  background: #000;
  border-radius: 50%;
  border: 2px solid #8B4513
}

.finger-cover {
  position: absolute;
  width: 20px;
  height: 20px;
  background: rgba(139, 69, 19, .8);
  border-radius: 50%;
  border: 2px solid #5D4037
}

.base-holes {
  position: absolute;
  right: 5%;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 5px
}

.base-hole {
  width: 8px;
  height: 8px;
  background: #000;
  border-radius: 50%;
  border: 1px solid #8B4513
}

.fingering-chart {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  justify-content: center
}

.finger-indicator {
  width: 40px;
  height: 40px;
  background: #2d2d2d;
  border: 2px solid #d4af37;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all .3s;
  font-weight: bold;
  color: #d4af37
}

.finger-indicator.active {
  background: #d4af37;
  color: #000
}

/* -------- 编钟 -------- */
.bianzhong {
  width: 500px;
  height: 200px;
  position: relative;
  margin: 0 auto
}

.bianzhong-body {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
  padding-top: 20px
}

.bianzhong-bell {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform .3s;
  padding: 10px
}

.bianzhong-bell:hover {
  transform: translateY(-5px)
}

.bianzhong-bell.playing {
  transform: translateY(-10px);
  animation: bellRing .5s ease-in-out
}

@keyframes bellRing {

  0%,
  100% {
    transform: translateY(-10px) rotate(0)
  }

  25% {
    transform: translateY(-10px) rotate(5deg)
  }

  75% {
    transform: translateY(-10px) rotate(-5deg)
  }
}

.bianzhong-bell .bell {
  width: 40px;
  height: 50px;
  background: linear-gradient(45deg, #B8860B, #DAA520);
  border-radius: 50% 50% 40% 40%;
  border: 3px solid #8B4513;
  box-shadow: 0 4px 8px rgba(0, 0, 0, .3)
}

.bianzhong-bell .bell-handle {
  width: 10px;
  height: 15px;
  background: #8B4513;
  border-radius: 5px 5px 0 0
}

/* -------- 唢呐 -------- */
.suona-playground {
  text-align: center
}

.suona-container {
  position: relative;
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center
}

.suona-instrument {
  position: relative;
  width: 200px;
  height: 300px;
  display: flex;
  align-items: center
}

.reed {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 15px;
  height: 25px;
  background: #8B4513;
  border-radius: 8px 0 0 8px;
  cursor: pointer;
  z-index: 2
}

.reed-tip {
  position: absolute;
  right: -2px;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 15px;
  background: #FFD700;
  border-radius: 2px
}

.suona-core {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 30px;
  background: linear-gradient(45deg, #A0522D, #CD853F);
  border-radius: 0 8px 8px 0
}

.suona-body {
  position: absolute;
  left: 35px;
  top: 50%;
  transform: translateY(-50%);
  width: 120px;
  height: 25px;
  background: linear-gradient(45deg, #8B4513, #A0522D);
  border-radius: 0 12px 12px 0
}

.suona-hole {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 25px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all .3s
}

.suona-hole:hover {
  background: rgba(212, 175, 55, .1)
}

.suona-hole.playing {
  background: rgba(212, 175, 55, .2)
}

.hole-indicator {
  width: 12px;
  height: 12px;
  background: #000;
  border-radius: 50%;
  border: 2px solid #5D4037
}

.breath-effect {
  position: absolute;
  right: -10px;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background: #d4af37;
  border-radius: 50%;
  animation: breathPulse .5s ease-in-out infinite
}

@keyframes breathPulse {

  0%,
  100% {
    opacity: .5;
    transform: translateY(-50%) scale(1)
  }

  50% {
    opacity: 1;
    transform: translateY(-50%) scale(1.2)
  }
}

.suona-bell {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 60px;
  height: 80px
}

.bell-flare {
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, #A0522D, #CD853F);
  border-radius: 50% 0 0 50%;
  border: 3px solid #8B4513
}

.breath-indicator {
  margin-top: 20px;
  width: 100px;
  height: 30px;
  background: #2d2d2d;
  border: 2px solid #666;
  border-radius: 15px;
  position: relative;
  overflow: hidden
}

.breath-indicator.blowing {
  border-color: #d4af37
}

.breath-flow {
  width: 0%;
  height: 100%;
  background: linear-gradient(90deg, #d4af37, #FFD700);
  transition: width .3s ease
}

.breath-indicator.blowing .breath-flow {
  width: 100%;
  animation: breathFlow 2s ease-in-out infinite
}

@keyframes breathFlow {

  0%,
  100% {
    opacity: .7
  }

  50% {
    opacity: 1
  }
}

.breath-btn {
  margin-top: 10px;
  padding: 8px 16px;
  border: 2px solid #d4af37;
  background: rgba(212, 175, 55, .1);
  color: #d4af37;
  border-radius: 20px;
  cursor: pointer;
  transition: all .3s
}

.breath-btn:hover {
  background: rgba(212, 175, 55, .2)
}

/* -------- 箫 -------- */
.xiao-playground {
  text-align: center
}

.xiao-container {
  position: relative;
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center
}

.xiao-tube {
  position: relative;
  width: 300px;
  height: 60px;
  background: linear-gradient(45deg, #006400, #228B22);
  border-radius: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, .2)
}

.xiao-mouthpiece {
  position: absolute;
  left: 8%;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 30px;
  background: #8B4513;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center
}

.mouth-cut {
  width: 8px;
  height: 15px;
  background: #000;
  border-radius: 4px
}

.xiao-hole {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 25px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all .3s
}

.xiao-hole:hover {
  background: rgba(212, 175, 55, .1)
}

.xiao-hole.playing {
  background: rgba(212, 175, 55, .2)
}

.hole-outline {
  width: 14px;
  height: 14px;
  background: #000;
  border-radius: 50%;
  border: 2px solid #8B4513
}

.xiao-finger-cover {
  position: absolute;
  width: 18px;
  height: 18px;
  background: rgba(139, 69, 19, .8);
  border-radius: 50%;
  border: 2px solid #5D4037
}

.xiao-fingering {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 20px
}

.xiao-finger-btn {
  padding: 10px;
  background: #2d2d2d;
  border: 2px solid #d4af37;
  border-radius: 8px;
  cursor: pointer;
  transition: all .3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px
}

.xiao-finger-btn.covered {
  background: #d4af37;
  color: #000
}

.finger-number {
  font-weight: bold;
  font-size: 16px
}

.finger-name {
  font-size: 12px;
  opacity: .8
}

.grid-top-bar,
.play-top-bar {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 12px 0 20px;
}

.grid-top-bar button,
.play-top-bar button {
  padding: 6px 14px;
  border: 1px solid #d4af37;
  background: none;
  color: #d4af37;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.grid-top-bar button.active,
.play-top-bar button.active {
  background: #d4af37;
  color: #000;
}

.grid-top-bar,
.play-top-bar {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 12px 0 20px;
}

.grid-top-bar button,
.play-top-bar button {
  padding: 6px 14px;
  border: 1px solid #d4af37;
  background: none;
  color: #d4af37;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.grid-top-bar button.active,
.play-top-bar button.active {
  background: #d4af37;
  color: #000;
}

/* 箫指法按钮横排 */
.xiao-fingering {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
}
</style>