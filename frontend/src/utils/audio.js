export class AudioManager {
    constructor() {
        this.audioContext = null
        this.currentSources = new Set()
    }

    init() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)()
        }
        return this.audioContext
    }

    // 安全的 AudioParam 设置
    safeSetAudioParam(param, value, defaultValue = 0) {
        if (!param) return

        const numValue = parseFloat(value)
        if (!isNaN(numValue) && isFinite(numValue)) {
            try {
                param.value = numValue
            } catch (error) {
                console.warn('AudioParam set error:', error)
                param.value = defaultValue
            }
        } else {
            console.warn(`Invalid audio param value: ${value}, using default: ${defaultValue}`)
            param.value = defaultValue
        }
    }

    // 安全的播放音符
    playNoteSafe(frequency, duration = 1.0, type = 'sine') {
        const context = this.init()

        if (!frequency || !isFinite(frequency)) {
            console.warn('Invalid frequency:', frequency)
            return null
        }

        try {
            const oscillator = context.createOscillator()
            const gainNode = context.createGain()

            oscillator.type = type
            this.safeSetAudioParam(oscillator.frequency, frequency, 440)

            // 安全的音量包络
            const now = context.currentTime
            this.safeSetAudioParam(gainNode.gain, 0, 0)
            gainNode.gain.linearRampToValueAtTime(0.3, now + 0.05)
            gainNode.gain.exponentialRampToValueAtTime(0.001, now + duration * 0.8)

            oscillator.connect(gainNode)
            gainNode.connect(context.destination)

            oscillator.start(now)
            oscillator.stop(now + duration)

            const source = { oscillator, gainNode }
            this.currentSources.add(source)

            oscillator.onended = () => {
                this.currentSources.delete(source)
            }

            return source
        } catch (error) {
            console.error('Play note error:', error)
            return null
        }
    }

    stopAll() {
        this.currentSources.forEach(source => {
            try {
                source.oscillator.stop()
            } catch (error) {
                console.warn('Stop oscillator error:', error)
            }
        })
        this.currentSources.clear()
    }

    // 恢复音频上下文（解决浏览器自动暂停）
    resume() {
        if (this.audioContext && this.audioContext.state === 'suspended') {
            return this.audioContext.resume()
        }
        return Promise.resolve()
    }
}

// 全局音频管理器实例
export const audioManager = new AudioManager()