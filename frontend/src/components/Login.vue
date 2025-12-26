<template>
  <div class="login-container">
    <div class="login-background">
      <div class="music-note note-1">♪</div>
      <div class="music-note note-2">♫</div>
      <div class="music-note note-3">♬</div>
      <div class="music-note note-4">𝄞</div>
      <div class="music-note note-5">𝄡</div>
    </div>

    <div class="login-card">
      <div class="login-header">
        <h1>古典音乐</h1>
        <p>登入音律之境 · 聆听千年回响</p>
      </div>

      <!-- 登录表单 -->
      <div class="login-form" v-if="!showRegisterForm">
        <div class="form-group">
          <label for="username">
            <User class="icon" />
            用户名
          </label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名" @focus="playNote('C4')" />
        </div>

        <div class="form-group">
          <label for="password">
            <Lock class="icon" />
            密码
          </label>
          <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password" placeholder="请输入密码"
            @focus="playNote('E4')" />
          <button type="button" class="password-toggle" @click="togglePasswordVisibility">
            <View v-if="showPassword" />
            <Hide v-else />
          </button>
        </div>

        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span class="checkmark"></span>
            记住我
          </label>
          <a href="#" class="forgot-password" @click.prevent="showForgotPassword">忘记密码?</a>
        </div>

        <button class="login-btn" :class="{ 'loading': isLoading }" @click="handleLogin" :disabled="isLoading">
          <span v-if="!isLoading">登入音律之境</span>
          <div v-else class="loading-spinner"></div>
        </button>

        <div class="switch-form">
          还没有账号? <a href="#" @click.prevent="switchToRegister">注册新账号</a>
        </div>
      </div>

      <!-- 注册表单 -->
      <div class="register-form" v-else>
        <div class="form-group">
          <label for="reg-username">
            <User class="icon" />
            用户名
          </label>
          <input type="text" id="reg-username" v-model="regUsername" placeholder="请输入用户名" @focus="playNote('D4')" />
        </div>

        <div class="form-group">
          <label for="reg-password">
            <Lock class="icon" />
            密码
          </label>
          <input :type="showRegPassword ? 'text' : 'password'" id="reg-password" v-model="regPassword"
            placeholder="请输入密码" @focus="playNote('F4')" />
          <button type="button" class="password-toggle" @click="toggleRegPasswordVisibility">
            <View v-if="showRegPassword" />
            <Hide v-else />
          </button>
        </div>

        <div class="form-group">
          <label for="confirm-password">
            <Lock class="icon" />
            确认密码
          </label>
          <input :type="showConfirmPassword ? 'text' : 'password'" id="confirm-password" v-model="confirmPassword"
            placeholder="请再次输入密码" @focus="playNote('G4')" />
          <button type="button" class="password-toggle" @click="toggleConfirmPasswordVisibility">
            <View v-if="showConfirmPassword" />
            <Hide v-else />
          </button>
        </div>

        <button class="register-btn" :class="{ 'loading': isRegistering }" @click="handleRegister"
          :disabled="isRegistering">
          <span v-if="!isRegistering">注册账号</span>
          <div v-else class="loading-spinner"></div>
        </button>

        <div class="switch-form">
          已有账号? <a href="#" @click.prevent="switchToLogin">立即登录</a>
        </div>
      </div>

      <!-- 音乐键盘 -->
      <div class="music-keyboard">
        <div v-for="key in keyboardKeys" :key="key.note" class="music-key" :class="{ 'black': key.isBlack }"
          @click="playNote(key.note)">
          {{ key.isBlack ? '' : key.label }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { User, Lock, View, Hide } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 响应式数据
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const isLoading = ref(false)

// 注册相关数据
const showRegisterForm = ref(false)
const regUsername = ref('')
const regPassword = ref('')
const confirmPassword = ref('')
const showRegPassword = ref(false)
const showConfirmPassword = ref(false)
const isRegistering = ref(false)

// 音乐键盘配置
const keyboardKeys = ref([
  { note: 'C4', label: 'C', isBlack: false },
  { note: 'C#4', label: '', isBlack: true },
  { note: 'D4', label: 'D', isBlack: false },
  { note: 'D#4', label: '', isBlack: true },
  { note: 'E4', label: 'E', isBlack: false },
  { note: 'F4', label: 'F', isBlack: false },
  { note: 'F#4', label: '', isBlack: true },
  { note: 'G4', label: 'G', isBlack: false },
  { note: 'G#4', label: '', isBlack: true },
  { note: 'A4', label: 'A', isBlack: false },
  { note: 'A#4', label: '', isBlack: true },
  { note: 'B4', label: 'B', isBlack: false }
])

// 音频上下文和振荡器
let audioContext = null
let oscillators = {}

// 初始化音频
const initAudio = () => {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
  }
}

// 播放音符
const playNote = (note) => {
  if (!audioContext) initAudio()

  if (oscillators[note]) {
    oscillators[note].stop()
    delete oscillators[note]
  }

  const frequencies = {
    'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56,
    'E3': 164.81, 'F3': 174.61, 'F#3': 185.00, 'G3': 196.00,
    'G#3': 207.65, 'A3': 220.00, 'A#3': 233.08, 'B3': 246.94,
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
    'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
    'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
    'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
    'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
    'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77
  }
  const frequency = frequencies[note]

  if (!frequency || !isFinite(frequency) || frequency <= 0) {
    const safeFrequency = 440.00
    playSafeNote(safeFrequency)
    return
  }

  function playSafeNote(frequency, note = 'unknown') {
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()

    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)

    oscillator.type = 'sine'
    oscillator.frequency.value = frequency

    const currentTime = audioContext.currentTime
    if (isFinite(currentTime)) {
      gainNode.gain.setValueAtTime(0.3, currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, currentTime + 1)
    }

    oscillator.start(currentTime)
    oscillator.stop(currentTime + 1)

    oscillators[note] = oscillator
  }

  playSafeNote(frequency, note)
}

// 切换密码可见性
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
  playNote('G4')
}

const toggleRegPasswordVisibility = () => {
  showRegPassword.value = !showRegPassword.value
  playNote('G4')
}

const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value
  playNote('G4')
}

// 检查本地保存的用户名
const checkRememberedUser = () => {
  try {
    const remembered = localStorage.getItem('rememberedUser')
    if (remembered) {
      username.value = remembered
      rememberMe.value = true
      console.log('找到记住的用户名:', remembered)
    }

    // 检查是否已登录
    const savedUser = localStorage.getItem('user')
    const savedToken = localStorage.getItem('token')

    if (savedUser && savedToken) {
      console.log('检测到已登录用户，自动跳转')
      // 自动触发登录成功
      setTimeout(() => {
        emit('login-success', {
          username: JSON.parse(savedUser).username,
          rememberMe: true
        })
      }, 500)
    }
  } catch (error) {
    console.error('检查记住的用户失败:', error)
  }
}

// 处理登录
const handleLogin = async () => {
  if (!username.value || !password.value) {
    ElMessage.error('请输入用户名和密码')
    return
  }
  try {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
    const res = await response.json()   // ← 这里必须接收
    if (res.success) {
      localStorage.setItem('user', JSON.stringify(res.user))
      localStorage.setItem('token', res.token)
      // 播放登录音效
      const melody = ['C4', 'E4', 'G4', 'C5']
      melody.forEach((n, i) => setTimeout(() => playNote(n), i * 200))
      ElMessage.success(`欢迎回来，${res.user.username}！`)
      emit('login-success', res.user)
    } else {
      ElMessage.error(res.message || '登录失败')
      playNote('C3')
    }
  } catch (e) {
    console.error('登录错误', e)
    ElMessage.error('网络连接失败，请检查后端服务')
  } finally {
    isLoading.value = false
  }
}

// 处理注册
const handleRegister = async () => {
  if (!regUsername.value || !regPassword.value || !confirmPassword.value) {
    ElMessage.error('请填写所有字段')
    return
  }

  if (regUsername.value.length < 3 || regUsername.value.length > 20) {
    ElMessage.error('用户名长度应为3-20个字符')
    return
  }

  if (regPassword.value.length < 6) {
    ElMessage.error('密码长度至少6位')
    playNote('C3')
    return
  }

  if (regPassword.value !== confirmPassword.value) {
    ElMessage.error('两次输入的密码不一致')
    playNote('C3')
    return
  }

  isRegistering.value = true

  try {
    const response = await fetch('http://localhost:5000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: regUsername.value,
        password: regPassword.value
      })
    })

    const result = await response.json()

    if (result.success) {
      // 播放注册成功音效
      const registerMelody = ['G4', 'B4', 'D5', 'G5']
      registerMelody.forEach((note, index) => {
        setTimeout(() => playNote(note), index * 200)
      })

      ElMessage.success('注册成功！请登录')

      // 自动填充登录表单并切换
      username.value = regUsername.value
      password.value = regPassword.value
      showRegisterForm.value = false

      // 清空注册表单
      regUsername.value = ''
      regPassword.value = ''
      confirmPassword.value = ''

    } else {
      ElMessage.error(result.message)
      playNote('C3')
    }

  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error('网络连接失败，请检查后端服务')
  } finally {
    isRegistering.value = false
  }
}

// 切换表单
const switchToRegister = () => {
  showRegisterForm.value = true
  playNote('A4')
}

const switchToLogin = () => {
  showRegisterForm.value = false
  playNote('A4')
}

// 忘记密码
const showForgotPassword = () => {
  ElMessage.info('请联系管理员重置密码')
  playNote('B4')
}

// 定义emit
const emit = defineEmits(['login-success'])

// 键盘事件监听
const handleKeyPress = (event) => {
  if (event.key === 'Enter') {
    if (showRegisterForm.value) {
      handleRegister()
    } else {
      handleLogin()
    }
  }
}

// 生命周期函数
onMounted(() => {
  initAudio()
  document.addEventListener('keypress', handleKeyPress)
  checkRememberedUser()
})

onUnmounted(() => {
  document.removeEventListener('keypress', handleKeyPress)
  Object.values(oscillators).forEach(osc => {
    if (osc) osc.stop()
  })
})
</script>

<style scoped>
/* 样式保持不变，使用原来的样式 */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a1d 0%, #2d1b1b 50%, #1a1a1d 100%);
  position: relative;
  overflow: hidden;
  font-family: STKaiti, KaiTi, serif;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.music-note {
  position: absolute;
  font-size: 2rem;
  color: rgba(212, 175, 55, 0.1);
  animation: float 6s ease-in-out infinite;
}

.note-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.note-2 {
  top: 60%;
  left: 85%;
  animation-delay: 1s;
}

.note-3 {
  top: 80%;
  left: 15%;
  animation-delay: 2s;
}

.note-4 {
  top: 30%;
  left: 80%;
  animation-delay: 3s;
}

.note-5 {
  top: 70%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }

  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

.login-card {
  background: rgba(26, 26, 29, 0.95);
  border: 1px solid #d4af37;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2);
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  font-size: 2.5rem;
  color: #d4af37;
  margin-bottom: 8px;
  font-weight: normal;
}

.login-header p {
  color: #aaa;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 20px;
  position: relative;
}

.form-group label {
  display: flex;
  align-items: center;
  color: #d4af37;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 6px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #d4af37;
  box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 38px;
  background: none;
  border: none;
  color: #d4af37;
  cursor: pointer;
  padding: 4px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  color: #aaa;
  cursor: pointer;
}

.remember-me input {
  display: none;
}

.checkmark {
  width: 16px;
  height: 16px;
  border: 1px solid #d4af37;
  border-radius: 3px;
  margin-right: 8px;
  position: relative;
  transition: all 0.3s ease;
}

.remember-me input:checked+.checkmark {
  background: #d4af37;
}

.remember-me input:checked+.checkmark::after {
  content: '✓';
  position: absolute;
  color: #000;
  font-size: 12px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.forgot-password {
  color: #d4af37;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #fff;
}

.login-btn,
.register-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #d4af37, #b8941f);
  border: none;
  border-radius: 6px;
  color: #000;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-btn:hover:not(:disabled),
.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
}

.login-btn:disabled,
.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid #000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.switch-form {
  text-align: center;
  margin-top: 20px;
  color: #aaa;
  font-size: 0.9rem;
}

.switch-form a {
  color: #d4af37;
  text-decoration: none;
  transition: color 0.3s ease;
}

.switch-form a:hover {
  color: #fff;
}

.music-keyboard {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  position: relative;
  height: 120px;
}

.music-key {
  width: 30px;
  height: 80px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 0 0 4px 4px;
  margin: 0 1px;
  cursor: pointer;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 8px;
  font-size: 0.7rem;
  color: #333;
  transition: all 0.1s ease;
  user-select: none;
}

.music-key:hover {
  background: #f0f0f0;
}

.music-key:active {
  background: #d4af37;
}

.music-key.black {
  width: 20px;
  height: 50px;
  background: #333;
  border: 1px solid #000;
  color: #fff;
  position: absolute;
  z-index: 2;
  margin: 0;
}

.music-key.black:nth-child(2) {
  left: 21px;
}

.music-key.black:nth-child(4) {
  left: 52px;
}

.music-key.black:nth-child(6) {
  left: 114px;
}

.music-key.black:nth-child(8) {
  left: 145px;
}

.music-key.black:nth-child(10) {
  left: 176px;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
    margin: 20px;
  }

  .login-header h1 {
    font-size: 2rem;
  }

  .music-keyboard {
    transform: scale(0.8);
  }
}
</style>