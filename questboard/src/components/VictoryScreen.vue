<script setup>
import { onMounted, ref } from 'vue'
import { useQuestStore } from '../stores/quest.js'
import gsap from 'gsap'

const store = useQuestStore()
const task = ref(store.lastCompleted)

onMounted(() => {
  gsap.from('.victory-paper', { scale: 0, opacity: 0, duration: 0.8, ease: 'elastic.out(1, 0.6)' })
  // Confetti particles
  for (let i = 0; i < 30; i++) {
    const el = document.createElement('div')
    el.className = 'confetti'
    el.style.left = Math.random() * 100 + '%'
    el.style.background = ['#e8c547','#c9a84c','#4a7c59','#94448c','#e84040'][i % 5]
    el.style.animationDelay = Math.random() * 2 + 's'
    document.querySelector('.victory-overlay')?.appendChild(el)
  }
})
</script>

<template>
  <div class="victory-overlay" @click="store.closeVictory">
    <div class="victory-paper">
      <div class="victory-seal">✦</div>
      <h2>🏆 任务完成！</h2>
      <p class="victory-text">
        「{{ task?.name }}」已被击败！<br>
        村庄重获和平。<br>
        <span class="reward">赏金 +{{ task?.reward }} 金币</span>
      </p>
      <button class="close-btn" @click="store.closeVictory">关闭</button>
    </div>
  </div>
</template>

<style scoped>
.victory-overlay { position: fixed; inset: 0; z-index: 300; background: rgba(0,0,0,.85); display: flex; align-items: center; justify-content: center; overflow: hidden; }
.victory-paper { width: 420px; background: linear-gradient(180deg, #f4e4c1, #e0c696); border: 3px solid var(--gold); border-radius: 8px; padding: 40px; text-align: center; box-shadow: 0 0 60px rgba(200,168,72,.3); position: relative; }
.victory-seal { position: absolute; top: -24px; left: 50%; transform: translateX(-50%); font-size: 40px; color: var(--gold); }
.victory-paper h2 { font-family: 'Cinzel', serif; color: var(--gold); font-size: 24px; margin-bottom: 16px; }
.victory-text { font-size: 18px; color: var(--ink); line-height: 2; }
.reward { color: #8b6914; font-weight: bold; font-size: 20px; }
.close-btn { margin-top: 20px; padding: 8px 24px; background: var(--red); color: #fff; border: none; border-radius: 6px; cursor: pointer; font-family: 'Cinzel', serif; font-size: 14px; }

.confetti { position: absolute; top: -10px; width: 8px; height: 8px; border-radius: 50%; animation: fall 3s linear forwards; }
@keyframes fall { to { top: 110vh; } }
</style>
