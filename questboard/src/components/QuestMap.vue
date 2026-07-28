<script setup>
import { useQuestStore } from '../stores/quest.js'
import { useAudioStore } from '../stores/audio.js'
import QuestCard from './QuestCard.vue'
import gsap from 'gsap'
import { onMounted, computed, ref } from 'vue'

const store = useQuestStore()
const audio = useAudioStore()
const emit = defineEmits(['openEditor', 'openHall', 'openFocus'])
const page = ref('today')

onMounted(async () => {
  await store.load()
  gsap.from('.card-wrap', { opacity:0, y:20, scale:.95, stagger:.06, duration:.4, ease:'power2.out' })
})

const today = () => store.questToday()

const todayCompleted = computed(() => {
  const td = today()
  return store.completedTasks.filter(t => t.date === td || t.created_at?.startsWith(td))
})

const visibleTasks = computed(() => {
  const qt = today()
  if (page.value === 'today') return store.activeTasks.filter(t => !t.date || t.date <= qt)
  if (page.value === 'tomorrow') {
    const dt = new Date(qt); dt.setDate(dt.getDate() + 1)
    return store.activeTasks.filter(t => t.date === dt.toISOString().slice(0, 10))
  }
  return []
})

const futureGroups = computed(() => {
  const qt = today()
  const tasks = store.activeTasks.filter(t => t.date && t.date > qt)
  const map = {}
  tasks.forEach(t => {
    if (!map[t.date]) map[t.date] = []
    map[t.date].push(t)
  })
  return Object.entries(map).sort((a, b) => a[0].localeCompare(b[0])).map(([date, tasks]) => ({ date, tasks }))
})

function onComplete(id) { store.completeTask(id) }
function onDelete(id) { store.deleteTask(id) }

function dayLabel(s) {
  const w = ['日','一','二','三','四','五','六']
  return s + ' (' + w[new Date(s).getDay()] + ')'
}
</script>

<template>
  <div class="quest-map">
    <header class="map-header">
      <div class="header-left">
        <svg class="heraldry" width="40" height="44" viewBox="0 0 40 44">
          <defs><linearGradient id="hgold" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#f0d060"/><stop offset="100%" stop-color="#8b6914"/></linearGradient></defs>
          <path d="M20 2 L34 8 L34 23 Q34 34 20 40 Q6 34 6 23 L6 8 Z" fill="none" stroke="url(#hgold)" stroke-width="1.5"/>
          <!-- Crossed swords -->
          <line x1="10" y1="28" x2="30" y2="12" stroke="var(--gold)" stroke-width="1.5"/>
          <line x1="8" y1="26" x2="32" y2="14" stroke="var(--gold-dim)" stroke-width="0.8"/>
          <line x1="30" y1="28" x2="10" y2="12" stroke="var(--gold)" stroke-width="1.5"/>
          <line x1="32" y1="26" x2="8" y2="14" stroke="var(--gold-dim)" stroke-width="0.8"/>
          <!-- Guards -->
          <line x1="16" y1="18" x2="24" y2="22" stroke="var(--gold)" stroke-width="2"/>
          <line x1="24" y1="18" x2="16" y2="22" stroke="var(--gold)" stroke-width="2"/>
        </svg>
        <h1 class="title">冒险者公会 · 悬赏版</h1>
      </div>
      <div class="header-right">
        <div class="stat-badge"><span class="stat-icon">💰</span><span class="stat-val">{{ store.gold }}</span></div>
        <div class="stat-badge"><span class="stat-icon">🏆</span><span class="stat-val">{{ store.epicCount }}</span></div>
        <button class="hall-btn" @click="emit('openHall')">🏛 荣誉殿堂</button>
        <button class="focus-mini-btn" @click="emit('openFocus')" title="专注模式">⏳</button>
        <button class="mute-mini-btn" @click="audio.toggleMute()" :title="audio.muted ? '取消静音' : '静音'">{{ audio.muted ? '🔇' : '🔊' }}</button>
      </div>
    </header>

    <div class="page-tabs">
      <button :class="['tab-btn', { active: page==='today' }]" @click="page='today'">今日悬赏</button>
      <button :class="['tab-btn', { active: page==='tomorrow' }]" @click="page='tomorrow'">明日悬赏</button>
      <button :class="['tab-btn', { active: page==='future' }]" @click="page='future'">📅 已排期</button>
    </div>

    <div class="board-area">
      <div class="cards-area" v-if="store.loaded">
        <!-- 今日/明日: 平铺 -->
        <template v-if="page!=='future'">
          <template v-for="(t,i) in visibleTasks" :key="t.id">
            <div class="card-wrap" v-if="t.name">
              <QuestCard :task="t" @complete="onComplete(t.id)" @delete="onDelete(t.id)" />
            </div>
          </template>
          <div v-if="visibleTasks.length===0" class="empty-state">
            <div class="empty-glow"></div>
            <div class="empty-scroll">
              <div class="empty-icon">📜</div>
              <p>悬赏板空空如也</p>
              <p class="hint">点击右下角魔导齿轮张贴悬赏</p>
            </div>
          </div>
        </template>
        <!-- 已排期: 按日期分组 -->
        <template v-else>
          <div v-for="g in futureGroups" :key="g.date" class="future-block">
            <div class="future-date">{{ dayLabel(g.date?.slice(5)) }}</div>
            <div class="future-cards">
              <div v-for="(t,i) in g.tasks" :key="t.id" class="card-wrap">
                <QuestCard :task="t" @complete="onComplete(t.id)" @delete="onDelete(t.id)" />
              </div>
            </div>
          </div>
          <div v-if="futureGroups.length===0" class="empty-state">
            <div class="empty-glow"></div>
            <div class="empty-scroll">
              <div class="empty-icon">📜</div>
              <p>暂无排期悬赏</p>
              <p class="hint">张贴悬赏时选择未来日期即可排期</p>
            </div>
          </div>
        </template>
      </div>
      <div v-if="todayCompleted.length" class="completed-section">
        <div class="section-divider"><span>今日已完成</span></div>
        <div class="completed-cards">
          <div v-for="t in todayCompleted" :key="t.id" class="done-chip">
            <span class="done-check">✓</span> {{ t.name?.slice(0,15)||'' }}
            <button class="del-btn" @click="store.deleteTask(t.id)">×</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quest-map { flex:1; display:flex; flex-direction:column; padding:10px 16px 14px; overflow-y:auto; position:relative; z-index:1; }

.map-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; padding:10px 18px;
  background:linear-gradient(180deg, rgba(36,24,16,.92), rgba(26,16,8,.88));
  border:1px solid rgba(200,168,72,.2); border-radius:8px; }
.header-left { display:flex; align-items:center; gap:10px; }
.heraldry { filter:drop-shadow(0 0 4px rgba(200,168,72,.3)); }
.title { font-family:'Cinzel',serif; font-size:20px; font-weight:900; letter-spacing:2px;
  background:linear-gradient(90deg, var(--copper-dark) 0%, var(--gold-bright) 25%, #fff 50%, var(--gold-bright) 75%, var(--copper-dark) 100%);
  background-size:200% auto; -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text; animation:shimmer 3s linear infinite; }
@keyframes shimmer { to{background-position:200% center} }
.header-right { display:flex; gap:10px; align-items:center; }
.stat-badge { display:flex; align-items:center; gap:4px; background:rgba(200,168,72,.08); border:1px solid rgba(200,168,72,.2); border-radius:14px; padding:4px 12px; }
.stat-icon { font-size:14px; } .stat-val { color:var(--gold-bright); font-size:14px; font-weight:bold; }
.hall-btn { display:flex; align-items:center; gap:4px; background:rgba(200,168,72,.1); border:1px solid rgba(200,168,72,.25); color:var(--gold-dim); padding:6px 14px; border-radius:14px; cursor:pointer; font-family:'Cinzel',serif; font-size:12px; transition:all .2s; }
.hall-btn:hover { background:rgba(200,168,72,.25); color:var(--gold-bright); }

.focus-mini-btn, .mute-mini-btn { background:rgba(0,0,0,.2); border:1px solid rgba(200,168,72,.15); border-radius:6px; padding:4px 8px; cursor:pointer; font-size:14px; transition:all .2s; color:rgba(200,168,72,.5); }
.focus-mini-btn:hover, .mute-mini-btn:hover { background:rgba(200,168,72,.1); color:var(--gold-bright); }

.page-tabs { display:flex; gap:4px; margin-bottom:8px; padding:0 4px; }
.tab-btn { padding:5px 14px; background:rgba(36,24,16,.4); border:1px solid rgba(200,168,72,.15); border-radius:6px 6px 0 0; color:var(--text-warm); cursor:pointer; font-family:'Cinzel',serif; font-size:12px; transition:all .2s; }
.tab-btn:hover { background:rgba(200,168,72,.1); }
.tab-btn.active { background:rgba(200,168,72,.15); border-color:var(--gold); color:var(--gold-bright); }

.date-badge { position:absolute; bottom:4px; right:30px; font-size:10px; background:rgba(200,168,72,.15); padding:1px 6px; border-radius:4px; color:var(--gold-dim); z-index:2; }

.future-block { width:100%; margin-bottom:16px; }
.future-date { font-family:'Cinzel',serif; font-size:13px; color:var(--gold); padding:6px 12px; background:rgba(200,168,72,.06); border:1px solid rgba(200,168,72,.15); border-radius:6px 6px 0 0; }
.future-cards { display:flex; flex-wrap:wrap; gap:16px; padding:10px 0; background:rgba(36,24,16,.2); border:1px solid rgba(200,168,72,.08); border-top:none; border-radius:0 0 6px 6px; }

.board-area { flex:1; background:rgba(36,24,16,.5); border:3px solid var(--board-border);
  border-radius:8px; box-shadow:inset 0 0 60px rgba(0,0,0,.4), 0 0 0 6px var(--oak-mid), 0 0 0 8px var(--board-border);
  padding:12px; margin:4px; overflow-y:auto;
  background-image:url("data:image/svg+xml,%3Csvg width='200' height='200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.7' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E"); }

/* Rivets on board corners */
.board-area::before,.board-area::after { content:''; position:absolute; width:12px; height:12px; border-radius:50%;
  background:radial-gradient(circle at 40% 35%, rgba(200,168,72,.6), var(--copper-dark));
  box-shadow:0 0 4px rgba(0,0,0,.5); }
.board-area::before { top:-8px; left:-8px; } .board-area::after { top:-8px; right:-8px; }

.cards-area { display:flex; flex-wrap:wrap; gap:16px; align-content:flex-start; padding:4px 0; }
.card-wrap { transition:all .2s; }
.card-wrap:nth-child(odd) { transform:rotate(.3deg); }
.card-wrap:nth-child(even) { transform:rotate(-.3deg); }
.card-wrap:hover { transform:scale(1.04) translateY(-4px)!important; z-index:999!important; }

.empty-state { width:100%; display:flex; justify-content:center; align-items:center; padding:80px 0; position:relative; }
.empty-glow { position:absolute; width:200px; height:200px; background:radial-gradient(circle, rgba(200,168,72,.1) 0%, transparent 70%); border-radius:50%; }
.empty-scroll { text-align:center; position:relative; }
.empty-icon { font-size:48px; margin-bottom:16px; opacity:.5; }
.empty-scroll p { color:var(--ink-light); font-size:18px; }
.empty-scroll .hint { font-size:14px; margin-top:8px; color:rgba(107,80,64,.5); }

.completed-section { margin-top:12px; }
.section-divider { display:flex; align-items:center; gap:12px; margin-bottom:10px; color:var(--gold-dim); font-size:12px; font-family:'Cinzel',serif; }
.section-divider::after,.section-divider::before { content:''; flex:1; height:1px; background:rgba(200,168,72,.15); }
.completed-cards { display:flex; flex-wrap:wrap; gap:8px; }
.done-chip { display:flex; align-items:center; gap:6px; background:rgba(90,144,96,.08); border:1px solid rgba(90,144,96,.2); color:var(--success); padding:4px 12px; border-radius:14px; font-size:13px; }
.done-check { font-weight:bold; }
.del-btn { background:none; border:none; color:var(--danger); cursor:pointer; font-size:12px; opacity:.6; }
.del-btn:hover { opacity:1; }
</style>
