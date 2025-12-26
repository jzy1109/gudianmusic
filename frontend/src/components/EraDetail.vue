<template>
    <section class="era-detail">
        <!-- 第5章 路由 - 编程式导航 -->
        <h1>{{ era.title }} · {{ era.period }}</h1>
        <p class="era-desc">{{ era.desc }}</p>

        <h3>代表音乐家</h3>
        <!-- 第2章-列表渲染 -->
        <ul>
            <li v-for="musician in era.musicians" :key="musician">{{ musician }}</li>
        </ul>

        <h3>重要事件</h3>
        <ul>
            <li v-for="event in era.events" :key="event">{{ event }}</li>
        </ul>
                <button class="back" @click="goBack">← 返回音乐起源</button>
    </section>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'// 第5章 路由 - 路由相关API

const route = useRoute()
const router = useRouter()
// 第5章 路由 - 获取动态路由参数
const eraId = route.params.eraId

const eras = {
    subjectivist: {
        id: 'subjectivist',
        title: '主观音乐时代',
        period: '20世纪初',
        desc: '主观音乐时代强调个人情感表达和主观体验，音乐作品更加注重内心世界的描绘。',
        musicians: ['勋伯格', '韦伯恩'],
        events: ['十二音体系的提出', '序列音乐的发展']
    },
    nationalism: {
        id: 'nationalism',
        title: '民族主义时代',
        period: '20世纪中期',
        desc: '民族主义音乐时代各国作曲家开始挖掘本民族音乐元素，形成独特的民族音乐风格。',
        musicians: ['西贝柳斯', '德彪西'],
        events: ['民族乐派的兴起', '世界音乐的多元化']
    },
    neoclassicism: {
        id: 'neoclassicism',
        title: '新古典主义时代',
        period: '20世纪末',
        desc: '新古典主义音乐回归古典形式，但运用现代和声和创作技法，形成新的音乐语言。',
        musicians: ['普罗科菲耶夫', '斯特拉文斯基'],
        events: ['新古典主义的复兴', '现代音乐的探索']
    },
    romanticism: {
        id: 'romanticism',
        title: '浪漫主义时代',
        period: '19世纪',
        desc: '浪漫主义音乐强调情感表达和个人主义，作品充满激情和想象力。',
        musicians: ['贝多芬', '肖邦'],
        events: ['浪漫主义音乐的兴起', '音乐表达的深化']
    },
    classical: {
        id: 'classical',
        title: '古典主义时代',
        period: '18世纪',
        desc: '古典主义音乐追求平衡、清晰和形式美，奏鸣曲和交响乐形式得到完善。',
        musicians: ['莫扎特', '海顿'],
        events: ['奏鸣曲形式的确立', '室内乐的发展']
    },
    baroque: {
        id: 'baroque',
        title: '巴洛克时代',
        period: '17世纪',
        desc: '巴洛克音乐以复杂的对位法和装饰性为特点，情感表达强烈而夸张。',
        musicians: ['巴赫', '亨德尔'],
        events: ['巴洛克风格的形成', '歌剧的诞生']
    },
    renaissance: {
        id: 'renaissance',
        title: '文艺复兴时代',
        period: '16世纪',
        desc: '文艺复兴音乐追求和谐与人本主义，复调音乐达到高峰。',
        musicians: ['帕莱斯特里纳', '拉索'],
        events: ['文艺复兴运动的影响', '音乐理论的发展']
    }
}
// 第2章-计算属性
const era = computed(() => eras[eraId] || {})

function goBack() {
    // 第5章 路由 - 编程式导航
    router.push('/')
}
</script>

<style scoped>
.era-detail {
    padding: 40px;
    color: #eee;
    font-family: STKaiti, KaiTi, serif;
    background: #1a1a1a;
    min-height: 100vh;
}

.back {
    background: none;
    border: 1px solid #d4af37;
    color: #d4af37;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 20px;
    transition: all 0.3s;
    font-size: 14px;
}

.back:hover {
    background: #d4af37;
    color: #000;
}

h1 {
    color: #d4af37;
    margin-bottom: 20px;
    font-size: 2.5em;
}

.era-desc {
    font-size: 18px;
    line-height: 1.8;
    margin-bottom: 30px;
    color: #ccc;
}

h3 {
    color: #d4af37;
    margin: 30px 0 15px;
    font-size: 1.5em;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    margin-bottom: 10px;
    padding: 10px 15px;
    background: #2d2d2d;
    border-radius: 6px;
    border-left: 4px solid #d4af37;
    transition: all 0.3s;
}

li:hover {
    background: #3d3d3d;
    transform: translateX(5px);
}
</style>