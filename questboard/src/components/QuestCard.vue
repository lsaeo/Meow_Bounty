<script setup>
import { ref, computed } from 'vue'
import gsap from 'gsap'

const props = defineProps({ task: Object })
const emit = defineEmits(['complete', 'delete'])

const cardRef = ref(null)
const rotateX = ref(0); const rotateY = ref(0); const glowX = ref(50); const glowY = ref(50)

const diffCfg = {
  '普通': { border:'#5a9060', glow:'rgba(90,144,96,.3)', stars:1, bg:'rgba(90,144,96,.06)', badgeBg:'rgba(90,144,96,.18)' },
  '困难': { border:'#d2a030', glow:'rgba(210,160,48,.3)', stars:3, bg:'rgba(210,160,48,.06)', badgeBg:'rgba(210,160,48,.18)' },
  '史诗': { border:'#b080d0', glow:'rgba(176,128,208,.3)', stars:5, bg:'rgba(176,128,208,.06)', badgeBg:'rgba(176,128,208,.18)' },
}
const d = computed(() => diffCfg[props.task.difficulty] || diffCfg['普通'])

function onMouseMove(e) { if(!cardRef.value) return; const r=cardRef.value.getBoundingClientRect(), x=e.clientX-r.left, y=e.clientY-r.top; rotateX.value=((y/r.height)-.5)*6; rotateY.value=((x/r.width)-.5)*-6; glowX.value=(x/r.width)*100; glowY.value=(y/r.height)*100 }
function onMouseLeave() { rotateX.value=0; rotateY.value=0; glowX.value=50; glowY.value=50 }
function onComplete() { if(props.task.completed) return; gsap.to(cardRef.value,{scale:.9,duration:.08,yoyo:true,repeat:1,onComplete:()=>emit('complete')}) }
</script>

<template>
<div ref="cardRef" :class="['quest-card',{completed:task.completed}]"
     :style="{transform:`perspective(600px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`, borderColor:d.border}"
     @mousemove="onMouseMove" @mouseleave="onMouseLeave">
  <div class="card-shimmer" :style="{background:`linear-gradient(105deg,transparent 40%,${d.glow} 50%,transparent 60%)`}"></div>

  <!-- Stars -->
  <div class="stars-row"><span v-for="s in d.stars" :key="s" class="star" :class="{active:s<=d.stars}">★</span></div>

  <!-- Wax seal -->
  <div class="wax-seal" @click="onComplete" v-if="!task.completed">
    <svg width="30" height="32" viewBox="0 0 30 32">
      <circle cx="15" cy="16" r="13" fill="var(--wax)" stroke="var(--wax-bright)" stroke-width="1.5"/>
      <circle cx="15" cy="16" r="9" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="1"/>
      <line x1="9" y1="16" x2="21" y2="16" stroke="rgba(255,255,255,.3)" stroke-width="2"/>
      <line x1="15" y1="10" x2="15" y2="22" stroke="rgba(255,255,255,.3)" stroke-width="2"/>
    </svg>
  </div>
  <div class="wax-seal done" v-else>
    <svg width="30" height="32" viewBox="0 0 30 32">
      <circle cx="15" cy="16" r="13" fill="rgba(90,144,96,.25)" stroke="var(--success)" stroke-width="1.5"/>
      <text x="15" y="20" text-anchor="middle" fill="var(--success)" font-size="14">✓</text>
    </svg>
  </div>

  <div class="card-body">
    <div class="diff-pill" :style="{background:d.badgeBg,borderColor:d.border,color:d.border}">{{ d.stars===1?'◆':d.stars===3?'★':'▲' }} {{ task.difficulty }}</div>
    <h3 class="quest-title">{{ task.name }}</h3>
    <p class="quest-origin" v-if="task.original_name"><span class="origin-label">原文</span>{{ task.original_name }}</p>
    <div class="card-meta">
      <span>💰 {{ task.reward||20 }}</span><span class="sep">·</span>
      <span>📜 {{ task.client||'村庄长老' }}</span>
    </div>
  </div>
  <button class="del-x" @click="emit('delete')">
    <svg width="10" height="10" viewBox="0 0 10 10"><line x1="1" y1="1" x2="9" y2="9" stroke="currentColor" stroke-width="1.5"/><line x1="9" y1="1" x2="1" y2="9" stroke="currentColor" stroke-width="1.5"/></svg>
  </button>
  <div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>
</div>
</template>

<style scoped>
.quest-card { width:280px; min-height:130px; background:
    linear-gradient(135deg, #f8ecd4 0%, #ecdcc0 30%, #e0ccaa 100%);
  border:1.5px solid; border-radius:10px; padding:14px 12px 12px; position:relative;
  transition:transform .15s,box-shadow .3s; overflow:hidden;
  box-shadow:0 4px 16px rgba(0,0,0,.3); }
.quest-card::before { content:''; position:absolute; inset:0; opacity:.06; pointer-events:none;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
.quest-card:hover { box-shadow:0 8px 28px rgba(0,0,0,.45)!important; }
.quest-card.completed { opacity:.55; filter:grayscale(.2); }
.quest-card.completed .quest-title { text-decoration:line-through; color:var(--success); }

.card-shimmer { position:absolute; inset:0; opacity:0; transition:opacity .3s; pointer-events:none; }
.quest-card:hover .card-shimmer { opacity:.2; }

.stars-row { position:absolute; top:8px; right:34px; display:flex; gap:1px; }
.star { color:rgba(0,0,0,.1); font-size:13px; transition:color .3s; }
.star.active { color:var(--gold-bright); text-shadow:0 0 4px rgba(200,168,72,.5); }

.wax-seal { position:absolute; top:-10px; left:-8px; cursor:pointer; z-index:3; transition:transform .15s; width:34px; height:36px;
  background: radial-gradient(circle at 35% 30%, #e06050 0%, #a03028 40%, #6b1818 70%, #3a0c0c 100%);
  border-radius:50%; box-shadow:2px 3px 5px rgba(0,0,0,.5), inset 0 -2px 3px rgba(0,0,0,.35);
  display:flex; align-items:center; justify-content:center; }
.wax-seal:hover { transform:scale(1.15); filter:brightness(1.1); }
.wax-seal svg { display:none; }
.wax-seal::after { content:'✦'; color:rgba(255,255,255,.5); font-size:11px; }
.wax-seal.done { background:radial-gradient(circle at 35% 30%, #60a070 0%, #387848 40%, #1e4a2a 70%, #0a1a10 100%); }
.wax-seal.done::after { content:'✓'; color:rgba(255,255,255,.6); font-size:14px; font-weight:bold; }
.card-body { padding-left:12px; }
.diff-pill { display:inline-block; padding:2px 10px; border-radius:10px; border:1px solid; font-size:11px; font-weight:bold; margin-bottom:8px; }
.quest-title { font-size:15px; color:var(--ink); margin:4px 0; line-height:1.4; font-weight:600; }
.quest-origin { font-size:11px; color:var(--ink-light); margin-bottom:6px; display:flex; gap:6px; align-items:center; }
.origin-label { font-size:10px; background:rgba(107,80,64,.1); padding:1px 6px; border-radius:4px; }
.card-meta { display:flex; gap:8px; align-items:center; font-size:13px; color:var(--copper-dark); font-weight:600; }
.sep { color:var(--ink-light); }

.del-x { position:absolute; bottom:6px; right:6px; background:none; border:none; color:var(--wax); cursor:pointer; opacity:.35; transition:opacity .15s; padding:4px; }
.del-x:hover { opacity:1; }

.corner { position:absolute; width:10px; height:10px; opacity:.15; }
.corner::before,.corner::after { content:''; position:absolute; background:var(--copper-dark); }
.tl{top:4px;left:4px}.tl::before{top:0;left:0;width:100%;height:1px}.tl::after{top:0;left:0;width:1px;height:100%}
.tr{top:4px;right:4px}.tr::before{top:0;right:0;width:100%;height:1px}.tr::after{top:0;right:0;width:1px;height:100%}
.bl{bottom:4px;left:4px}.bl::before{bottom:0;left:0;width:100%;height:1px}.bl::after{bottom:0;left:0;width:1px;height:100%}
.br{bottom:4px;right:4px}.br::before{bottom:0;right:0;width:100%;height:1px}.br::after{bottom:0;right:0;width:1px;height:100%}
</style>
