<template>
    <section class="music-timeline">
        <h2>音乐发展史</h2>
        <div class="timeline-wrapper">
            <div class="timeline-track">
                <!-- 第2章-列表渲染 -->
                <div v-for="era in eras" :key="era.id" class="timeline-card" @click="navigateToEra(era.id)">
                    <!-- 第2章-样式绑定 -->
                    <h3 :style="{ color: era.color }">{{ era.title }}</h3>
                    <p>{{ era.period }}</p>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'// 第5章 路由 - 路由相关API

const router = useRouter()
const eras = ref([
    { id: 'subjectivist', title: '主观音乐时代', period: '20世纪初', color: '#FFD700' },
    { id: 'nationalism', title: '民族主义时代', period: '20世纪中期', color: '#32CD32' },
    { id: 'neoclassicism', title: '新古典主义时代', period: '20世纪末', color: '#6A5ACD' },
    { id: 'romanticism', title: '浪漫主义时代', period: '19世纪', color: '#FF69B4' },
    { id: 'classical', title: '古典主义时代', period: '18世纪', color: '#483D8B' },
    { id: 'baroque', title: '巴洛克时代', period: '17世纪', color: '#FF6347' },
    { id: 'renaissance', title: '文艺复兴时代', period: '16世纪', color: '#FF4500' }
])

function navigateToEra(eraId) {
    // 第5章 路由 - 编程式导航
    console.log('Navigating to era:', eraId);
    // 使用完整的路由路径
    router.push(`/era/${eraId}`);
}
</script>

<style scoped>
.music-timeline {
    padding: 40px 0;
    color: #eee;
    font-family: STKaiti, KaiTi, serif;
}

h2 {
    text-align: center;
    font-size: 32px;
    margin-bottom: 30px;
    color: #d4af37;
}

.timeline-wrapper {
    overflow-x: auto;
    scrollbar-width: thin;
    scrollbar-color: #d4af37 #2d2d2d;
}

.timeline-track {
    display: flex;
    gap: 24px;
    padding: 0 40px 20px;
    width: max-content;
}

.timeline-card {
    flex: 0 0 240px;
    background: #2d2d2d;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
}

.timeline-card:hover,
.timeline-card.active {
    transform: translateY(-6px);
    box-shadow: 0 8px 20px rgba(212, 175, 55, 0.35);
    border-color: #d4af37;
}

h3 {
    font-size: 24px;
    font-weight: bold;
    color: #d4af37;
    margin-bottom: 8px;
}

p {
    font-size: 16px;
    color: #ccc;
    line-height: 1.5;
}
</style>