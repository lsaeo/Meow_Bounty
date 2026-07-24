<script setup>
import { useQuestStore } from '../stores/quest.js'
import gsap from 'gsap'
import { onMounted } from 'vue'

const store = useQuestStore()
const emit = defineEmits(['close'])

onMounted(() => gsap.from('.hall-item', { opacity: 0, y: 30, stagger: 0.1, duration: 0.5 }))
</script>

<template>
  <div class="hall-overlay" @click.self="emit('close')">
    <div class="hall-panel">
      <h2 class="hall-title">🏛 荣誉殿堂</h2>
      <p class="hall-sub">已有 {{ store.completedTasks.length }} 项悬赏被完成</p>
      <div class="hall-grid">
        <div v-for="t in store.completedTasks" :key="t.id" class="hall-item">
          <div class="trophy-frame">
            <span class="trophy-icon">🏆</span>
          </div>
          <p class="trophy-name">{{ t.name?.slice(0, 16) || '...' }}</p>
          <p class="trophy-date">{{ t.created_at?.slice(0, 10) || '' }}</p>
        </div>
      </div>
      <button class="close-btn" @click="emit('close')">关闭</button>
    </div>
  </div>
</template>

<style scoped>
.hall-overlay { position: fixed; inset: 0; z-index: 250; background: rgba(0,0,0,.8); display: flex; align-items: center; justify-content: center; }
.hall-panel { width: 700px; max-height: 80vh; overflow-y: auto; background: linear-gradient(180deg, #2a1810, #1a0a04); border: 2px solid var(--gold); border-radius: 8px; padding: 30px; box-shadow: 0 8px 40px rgba(0,0,0,.7), inset 0 0 80px rgba(200,168,72,.05); }
.hall-title { font-family: 'Cinzel', serif; color: var(--gold-bright); font-size: 26px; text-align: center; }
.hall-sub { color: #8c7b6b; text-align: center; margin: 8px 0 20px; font-size: 14px; }
.hall-grid { display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; }
.hall-item { text-align: center; width: 130px; }
.trophy-frame { width: 80px; height: 80px; margin: 0 auto 8px; background: rgba(200,168,72,.15); border: 2px solid var(--gold); border-radius: 8px; display: flex; align-items: center; justify-content: center; }
.trophy-icon { font-size: 36px; }
.trophy-name { font-size: 12px; color: var(--gold); }
.trophy-date { font-size: 11px; color: #6b5344; }
.close-btn { display: block; margin: 20px auto 0; padding: 8px 24px; background: var(--red); color: #fff; border: none; border-radius: 6px; cursor: pointer; font-family: 'Cinzel', serif; font-size: 14px; }
</style>
