<script setup>
import { ref, onMounted } from 'vue'
import { useQuestStore } from './stores/quest.js'
import { useAudioStore } from './stores/audio.js'
import QuestMap from './components/QuestMap.vue'
import ScrollEditor from './components/ScrollEditor.vue'
import VictoryScreen from './components/VictoryScreen.vue'
import HallOfFame from './components/HallOfFame.vue'
import { useAchievementsStore } from './stores/achievements.js'
import BadgePopup from './components/BadgePopup.vue'
import WeeklyReport from './components/WeeklyReport.vue'
import FocusMode from './components/FocusMode.vue'
import { useWeeklyStore } from './stores/weekly.js'

const store = useQuestStore()
const audioStore = useAudioStore()
const achievementsStore = useAchievementsStore()
const weeklyStore = useWeeklyStore()
const showEditor = ref(false)
const showHall = ref(false)
const showFocus = ref(false)

onMounted(() => { setTimeout(() => weeklyStore.checkShow(), 500) })

function openEditor() { showEditor.value = true; audioStore.play('click') }
function closeEditor() { showEditor.value = false }

function minimize() { if (window.api) window.api.minimize() }
function toggleMaximize() { if (window.api) window.api.maximize() }
function closeWin() { if (window.api) { window.api.close() } else { window.close() } }
</script>

<template>
  <div class="app-shell">
    <div class="title-bar">
      <span class="title-bar-text">QuestPet · 冒险者公会</span>
      <div class="win-controls">
        <button class="win-btn" @click="minimize" title="最小化">─</button>
        <button class="win-btn" @click="toggleMaximize" title="最大化">☐</button>
        <button class="win-btn win-close" @click="closeWin" title="关闭">✕</button>
      </div>
    </div>
    <div class="particles">
      <span v-for="i in 30" :key="i" class="particle" :style="{
        left: Math.random() * 100 + '%', top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 8 + 's',
        animationDuration: 3 + Math.random() * 5 + 's',
        width: 1.5 + Math.random() * 3 + 'px', height: 1.5 + Math.random() * 3 + 'px'
      }"></span>
    </div>
    <QuestMap @open-editor="openEditor" @open-hall="showHall = true" @open-focus="showFocus = true" />
    <Transition name="scroll">
      <ScrollEditor v-if="showEditor" @close="closeEditor" />
    </Transition>
    <VictoryScreen v-if="store.showVictory" />
    <BadgePopup v-if="achievementsStore.showing" />
    <WeeklyReport v-if="weeklyStore.showReport" />
    <HallOfFame v-if="showHall" @close="showHall = false" />
    <FocusMode v-if="showFocus" @close="showFocus = false" />
    <button class="fab" @click="openEditor">
      <span class="material-symbols-outlined" style="font-size:24px;color:#fff;">edit</span>
    </button>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Noto+Serif+SC:wght@400;700&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');

:root {
  --oak-deep: #120a04; --oak-mid: #1a1008; --oak-light: #241810;
  --gold: #c9a84c; --gold-bright: #e8c860; --gold-dim: #8b6914;
  --amber: #e8a840; --amber-glow: rgba(232,168,64,.15);
  --parchment: #f4e4c1; --parchment-dark: #e0ccaa;
  --ink: #3b2814; --ink-light: #6b5040;
  --copper: #b87333; --copper-dark: #8b5a20;
  --wax: #8b2020; --wax-bright: #c04040;
  --text: #3b2814; --text-warm: #5a4030;
  --success: #5a9060; --danger: #c04040;
  --board-border: #3a1e0e;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Cormorant Garamond','Noto Serif SC',serif; background:var(--oak-deep); color:var(--text); overflow:hidden; height:100vh; }

.app-shell { height:100vh; padding-top:28px;
  background:
    radial-gradient(ellipse at 25% 30%, rgba(232,168,64,.2) 0%, transparent 40%),
    radial-gradient(ellipse at 75% 25%, rgba(220,150,50,.14) 0%, transparent 38%),
    radial-gradient(ellipse at 45% 70%, rgba(200,140,40,.12) 0%, transparent 40%),
    repeating-linear-gradient(90deg, var(--oak-deep) 0px, var(--oak-mid) 2px, var(--oak-deep) 4px, #1a0e04 6px, var(--oak-deep) 8px),
    linear-gradient(180deg, #0a0602 0%, var(--oak-deep) 15%, var(--oak-mid) 50%, var(--oak-deep) 100%);
  position:relative; display:flex; flex-direction:column; }

.particles { position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden; }
.particle { position:absolute; border-radius:50%; animation: floatUp linear infinite; opacity:0; }
.particle:nth-child(3n) { background:#fff8e0; width:2.5px; height:2.5px; box-shadow:0 0 14px rgba(255,240,200,.9), 0 0 28px rgba(240,180,60,.5); }
.particle:nth-child(3n+1) { background:#ffd080; width:3.5px; height:3.5px; box-shadow:0 0 18px rgba(255,210,120,.8), 0 0 32px rgba(220,150,40,.4); }
.particle:nth-child(3n+2) { background:#ffe0a0; width:2px; height:2px; box-shadow:0 0 10px rgba(255,224,160,.7); }
.particle:nth-child(5n) { width:4px; height:4px; box-shadow:0 0 22px rgba(255,240,200,1), 0 0 36px rgba(240,180,60,.6); animation-duration:4s; }
.particle:nth-child(7n) { animation:twinkle 2s ease-in-out infinite; }
@keyframes twinkle { 0%,100%{opacity:.2} 50%{opacity:.9} }
@keyframes floatUp { 0%{transform:translateY(0) scale(1); opacity:0} 10%{opacity:.9} 90%{opacity:.4} 100%{transform:translateY(-100vh) scale(.3); opacity:0} }

.fab { position:fixed; bottom:28px; right:28px; width:56px; height:56px; border-radius:50%; z-index:100;
  display:flex; align-items:center; justify-content:center; cursor:pointer; color:#fff;
  background: conic-gradient(from 0deg, var(--gold), var(--copper-dark), var(--gold-bright), var(--gold));
  border:2px solid var(--gold-bright);
  box-shadow: 0 4px 28px rgba(200,168,72,.4), 0 0 80px rgba(200,168,72,.12), inset 0 1px 0 rgba(255,255,255,.2);
  transition:all .3s; animation:fabPulse 3s ease-in-out infinite; }
@keyframes fabPulse { 50%{box-shadow:0 4px 36px rgba(200,168,72,.55),0 0 100px rgba(200,168,72,.18)} }
.fab:hover { transform:scale(1.12); }

.scroll-enter-active { animation:scrollIn .35s ease-out; }
.scroll-leave-active { animation:scrollIn .2s ease-in reverse; }
@keyframes scrollIn { from{opacity:0; transform:scale(.85)} to{opacity:1; transform:scale(1)} }

.title-bar { position:fixed; top:0; left:0; right:0; height:28px; z-index:200; display:flex; align-items:center; justify-content:space-between; padding:0 8px 0 14px;
  background:rgba(0,0,0,.6); -webkit-app-region:drag; user-select:none; }
.title-bar-text { font-family:'Cinzel',serif; font-size:11px; color:rgba(200,168,72,.4); letter-spacing:1px; }
.win-controls { display:flex; -webkit-app-region:no-drag; }
.win-btn { width:32px; height:22px; display:flex; align-items:center; justify-content:center; background:none; border:none; color:rgba(255,255,255,.4); cursor:pointer; font-size:14px; transition:all .15s; border-radius:4px; }
.win-btn:hover { background:rgba(255,255,255,.08); color:rgba(255,255,255,.8); }
.win-close:hover { background:#c04040; color:#fff; }
</style>
