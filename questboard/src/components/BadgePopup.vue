<script setup>
import { useAchievementsStore } from '../stores/achievements.js'
import { onMounted, ref, computed } from 'vue'
import gsap from 'gsap'

const store = useAchievementsStore()
const badgeRef = ref(null)
const current = computed(() => store.currentAchievement())

onMounted(() => {
  if (!badgeRef.value) return
  gsap.fromTo(badgeRef.value, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.7)' })
  const timer = setTimeout(() => done(), 5000)
  badgeRef.value._timer = timer
})

function done() {
  if (badgeRef.value?._timer) clearTimeout(badgeRef.value._timer)
  gsap.to(badgeRef.value, { scale: 0.8, opacity: 0, duration: 0.3, onComplete: () => store.onPopupClosed() })
}
</script>

<template>
  <div class="badge-overlay" @click.self="done">
    <div ref="badgeRef" class="badge-popup" v-if="current">
      <div class="badge-icon-circle">
        <span class="badge-icon">{{ current.icon }}</span>
        <span class="badge-star">✦</span>
      </div>
      <h2 class="badge-title">获得成就</h2>
      <h3 class="badge-name">{{ current.name }}</h3>
      <p class="badge-desc">{{ current.desc }}</p>
      <button class="badge-btn" @click="done">确认</button>
    </div>
  </div>
</template>

<style scoped>
.badge-overlay { position: fixed; inset: 0; z-index: 400; background: rgba(0,0,0,.6); display: flex; align-items: center; justify-content: center; backdrop-filter: blur(4px); }
.badge-popup { width: 320px; background: linear-gradient(180deg, #2a1a10 0%, #1a0e06 100%); border: 2px solid var(--gold); border-radius: 14px; padding: 30px 24px 24px; text-align: center; box-shadow: 0 8px 40px rgba(200,168,72,.3), 0 0 80px rgba(200,168,72,.1); }
.badge-icon-circle { width: 72px; height: 72px; margin: 0 auto 16px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #f0d060, #8b6914 70%, #4a3008); box-shadow: 0 4px 16px rgba(200,168,72,.4); display: flex; align-items: center; justify-content: center; position: relative; }
.badge-icon { font-size: 32px; }
.badge-star { position: absolute; top: -6px; right: -4px; color: var(--gold-bright); font-size: 16px; text-shadow: 0 0 6px rgba(240,208,96,.6); }
.badge-title { font-family: 'Cinzel', serif; font-size: 14px; color: var(--gold-dim); margin-bottom: 6px; }
.badge-name { font-family: 'Cinzel', serif; font-size: 22px; color: var(--gold-bright); margin-bottom: 8px; text-shadow: 0 2px 6px rgba(0,0,0,.4); }
.badge-desc { font-size: 15px; color: var(--text-warm); margin-bottom: 20px; }
.badge-btn { background: linear-gradient(135deg, var(--gold), var(--copper-dark)); border: none; color: #fff; padding: 10px 32px; border-radius: 20px; font-family: 'Cinzel', serif; font-size: 14px; cursor: pointer; box-shadow: 0 2px 8px rgba(200,168,72,.3); transition: all .2s; }
.badge-btn:hover { transform: scale(1.05); box-shadow: 0 4px 16px rgba(200,168,72,.5); }
</style>
