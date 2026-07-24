<script setup>
import { useWeeklyStore } from '../stores/weekly.js'
import gsap from 'gsap'
import { onMounted, ref } from 'vue'

const store = useWeeklyStore()
const panelRef = ref(null)
const r = store.report

onMounted(() => {
  gsap.fromTo(panelRef.value, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.5)' })
  const timer = setTimeout(() => done(), 8000)
  panelRef.value._timer = timer
})

function done() {
  if (panelRef.value?._timer) clearTimeout(panelRef.value._timer)
  gsap.to(panelRef.value, { scale: 0.85, opacity: 0, duration: 0.4, onComplete: () => store.close() })
}
</script>

<template>
  <div class="report-overlay" @click.self="done">
    <div ref="panelRef" class="report-panel" v-if="r">
      <h2 class="report-title">本周战报</h2>

      <div class="report-grid">
        <div class="stat-card">
          <div class="stat-icon">🏆</div>
          <div class="stat-value">{{ r.total }}</div>
          <div class="stat-label">本周完成</div>
          <div class="stat-diff" :class="r.total >= r.lastTotal ? 'up' : 'down'">
            {{ r.total >= r.lastTotal ? '↑' : '↓' }} 较上周
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-value">{{ r.gold }}</div>
          <div class="stat-label">获得金币</div>
          <div class="stat-diff" :class="r.gold >= r.lastGold ? 'up' : 'down'">
            {{ r.gold >= r.lastGold ? '↑' : '↓' }} 较上周
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">👑</div>
          <div class="stat-value">{{ r.epic }}</div>
          <div class="stat-label">史诗悬赏</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📜</div>
          <div class="stat-value name">{{ r.topClient }}</div>
          <div class="stat-label">最常委托人 ({{ r.topCount }}次)</div>
        </div>
      </div>

      <div class="report-bar-section">
        <div class="bar-label">本周 vs 上周</div>
        <div class="bar-row">
          <div class="bar-fill" :style="{ width: Math.max(r.total / Math.max(r.lastTotal, 1) * 50, 10) + '%' }">
            {{ r.total }}
          </div>
          <div class="bar-last" :style="{ width: '50%', opacity: 0.3 }">
            上周 {{ r.lastTotal }}
          </div>
        </div>
      </div>

      <button class="report-btn" @click="done">关闭</button>
    </div>
  </div>
</template>

<style scoped>
.report-overlay { position: fixed; inset: 0; z-index: 350; background: rgba(0,0,0,.65); display: flex; align-items: center; justify-content: center; backdrop-filter: blur(6px); }
.report-panel { width: 500px; background: linear-gradient(180deg, #241810 0%, #1a0e06 100%); border: 2px solid var(--gold); border-radius: 14px; padding: 28px 24px 24px; box-shadow: 0 8px 40px rgba(200,168,72,.3); }
.report-title { font-family: 'Cinzel', serif; font-size: 20px; color: var(--gold-bright); text-align: center; margin-bottom: 20px; letter-spacing: 2px; }
.report-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 18px; }
.stat-card { background: rgba(200,168,72,.06); border: 1px solid rgba(200,168,72,.2); border-radius: 10px; padding: 14px; text-align: center; }
.stat-icon { font-size: 24px; margin-bottom: 4px; }
.stat-value { font-size: 28px; font-weight: bold; color: var(--gold-bright); }
.stat-value.name { font-size: 16px; }
.stat-label { font-size: 12px; color: var(--text-warm); margin-top: 2px; }
.stat-diff { font-size: 11px; margin-top: 4px; }
.stat-diff.up { color: var(--success); }
.stat-diff.down { color: var(--danger); }

.report-bar-section { margin-bottom: 18px; }
.bar-label { font-size: 12px; color: var(--text-warm); margin-bottom: 6px; }
.bar-row { display: flex; height: 28px; border-radius: 6px; overflow: hidden; }
.bar-fill { background: linear-gradient(90deg, var(--gold), var(--copper-dark)); display: flex; align-items: center; justify-content: center; font-size: 13px; color: #fff; font-weight: bold; transition: width .5s; }
.bar-last { background: rgba(255,255,255,.1); display: flex; align-items: center; justify-content: center; font-size: 12px; color: var(--text-warm); }

.report-btn { display: block; margin: 0 auto; background: linear-gradient(135deg, var(--gold), var(--copper-dark)); border: none; color: #fff; padding: 10px 36px; border-radius: 20px; font-family: 'Cinzel', serif; font-size: 14px; cursor: pointer; }
.report-btn:hover { filter: brightness(1.1); }
</style>
