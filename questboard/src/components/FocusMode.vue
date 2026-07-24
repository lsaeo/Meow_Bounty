<script setup>
import { useFocusStore } from '../stores/focus.js'
import gsap from 'gsap'
import { onMounted, watch, ref, computed } from 'vue'

const store = useFocusStore()
const emit = defineEmits(['close'])
const presets = [25, 45, 60]
const selected = ref(25)
const quoteIdx = ref(0)
const quoteTimer = ref(null)
const particles = ref([])
const ringA = ref(null)
const ringB = ref(null)
const ringC = ref(null)

const quotes = [
  '专注是通往大师的唯一路径',
  '每一滴灵药，都是时间的凝聚',
  '此刻，没有过去，没有未来',
  '心流之中，万物寂静',
  '圣杯满溢之时，你已不同',
  '水滴石穿，非一日之功',
  '此刻的沉默，胜过千言万语',
  '专注之所向，即是你的世界',
]

const quote = computed(() => quotes[quoteIdx.value])

const runes = ['ᚠ','ᚢ','ᚦ','ᚨ','ᚱ','ᚲ','ᚷ','ᚹ','ᚺ','ᚾ','ᛁ','ᛃ']

const liquidY = computed(() => {
  const maxH = 83
  return 98 - maxH * store.progress
})

function start() {
  particles.value = []
  store.start(selected.value)
  gsap.from('.chalice-wrap', { scale: 1.1, duration: .3, ease: 'power2.out' })
  quoteIdx.value = 0
  quoteTimer.value = setInterval(() => {
    quoteIdx.value = (quoteIdx.value + 1) % quotes.length
  }, 15000)
  // Start rune rings spinning
  ;[ringA, ringB, ringC].forEach((r, i) => {
    if (r.value) gsap.to(r.value, { rotation: (i % 2 ? 360 : -360), duration: 8 + i * 6, repeat: -1, ease: 'none' })
  })
}

watch(() => store.done, (v) => {
  if (v) {
    clearInterval(quoteTimer.value)
    gsap.from('.reward-pop', { scale: 0, rotation: -30, duration: .6, ease: 'back.out(2)', delay: .3 })
    const pts = []
    for (let i = 0; i < 20; i++) {
      pts.push({ id: i, x: Math.random() * 60 - 30, y: Math.random() * 60 - 30, s: 2 + Math.random() * 4, d: .6 + Math.random() * .8 })
    }
    particles.value = pts
  }
})

onMounted(() => {
  gsap.from('.focus-panel', { opacity: 0, scale: .85, duration: .5, ease: 'power3.out' })
  gsap.from('.chalice-wrap', { y: 20, opacity: 0, duration: .6, delay: .1, ease: 'power2.out' })
  // Rune ring idle rotation
  ;[ringA, ringB, ringC].forEach((r, i) => {
    if (r.value) gsap.to(r.value, { rotation: 360, duration: 20 + i * 10, repeat: -1, ease: 'none' })
  })
})
</script>

<template>
  <div class="focus-overlay" @click.self="!store.running && emit('close')">
    <div class="starfield">
      <span v-for="i in 40" :key="i" class="star-dot" :style="{
        left: Math.random() * 100 + '%', top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 4 + 's',
        width: 1 + Math.random() * 2 + 'px', height: 1 + Math.random() * 2 + 'px'
      }"></span>
    </div>

    <div class="aura-glow" :class="{ breathing: !store.running, active: store.running }"></div>

    <div class="focus-panel">
      <button class="focus-close" @click="emit('close')" v-if="!store.running">&times;</button>

      <!-- Chalice + Rune Rings -->
      <div class="chalice-wrap">
        <!-- Rune Ring A (outer) -->
        <svg class="rune-ring ring-a" ref="ringA" viewBox="0 0 180 180" width="180" height="180">
          <circle cx="90" cy="90" r="78" fill="none" stroke="rgba(200,168,72,.08)" stroke-width="1"/>
          <text v-for="(r, i) in runes" :key="'a'+i"
            :x="90 + 74 * Math.cos(i * Math.PI / 6 - Math.PI / 2)"
            :y="90 + 74 * Math.sin(i * Math.PI / 6 - Math.PI / 2)"
            text-anchor="middle" dominant-baseline="central"
            fill="rgba(200,168,72,.4)" font-size="10" class="rune-char">{{ r }}</text>
        </svg>
        <!-- Rune Ring B (middle, opposite spin) -->
        <svg class="rune-ring ring-b" ref="ringB" viewBox="0 0 160 160" width="160" height="160">
          <circle cx="80" cy="80" r="68" fill="none" stroke="rgba(200,168,72,.06)" stroke-width="1"/>
          <text v-for="(r, i) in runes" :key="'b'+i"
            :x="80 + 64 * Math.cos(i * Math.PI / 6 + Math.PI / 6)"
            :y="80 + 64 * Math.sin(i * Math.PI / 6 + Math.PI / 6)"
            text-anchor="middle" dominant-baseline="central"
            fill="rgba(200,168,72,.25)" font-size="8" class="rune-char">{{ r }}</text>
        </svg>
        <!-- Rune Ring C (inner) -->
        <svg class="rune-ring ring-c" ref="ringC" viewBox="0 0 140 140" width="140" height="140">
          <circle cx="70" cy="70" r="58" fill="none" stroke="rgba(200,168,72,.05)" stroke-width="1"/>
          <text v-for="(r, i) in runes" :key="'c'+i"
            :x="70 + 54 * Math.cos(i * Math.PI / 6 + Math.PI / 3)"
            :y="70 + 54 * Math.sin(i * Math.PI / 6 + Math.PI / 3)"
            text-anchor="middle" dominant-baseline="central"
            fill="rgba(200,168,72,.2)" font-size="7" class="rune-char">{{ r }}</text>
        </svg>

        <!-- Magical Chalice SVG -->
        <div class="chalice-svg">
          <svg width="120" height="170" viewBox="0 0 120 170">
            <defs>
              <linearGradient id="glassGradC" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="rgba(180,160,220,.06)" />
                <stop offset="25%" stop-color="rgba(210,190,240,.18)" />
                <stop offset="45%" stop-color="rgba(255,255,255,.35)" />
                <stop offset="55%" stop-color="rgba(255,255,255,.4)" />
                <stop offset="75%" stop-color="rgba(210,190,240,.18)" />
                <stop offset="100%" stop-color="rgba(180,160,220,.06)" />
              </linearGradient>
              <linearGradient id="liquidGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#f8e080" />
                <stop offset="30%" stop-color="#f0d060" />
                <stop offset="65%" stop-color="#d4a830" />
                <stop offset="100%" stop-color="#906020" />
              </linearGradient>
              <linearGradient id="goldTrim" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#8b6914" />
                <stop offset="30%" stop-color="#e8c860" />
                <stop offset="50%" stop-color="#f8e890" />
                <stop offset="70%" stop-color="#e8c860" />
                <stop offset="100%" stop-color="#8b6914" />
              </linearGradient>
              <radialGradient id="liqGlow" cx="50%" cy="30%" r="60%">
                <stop offset="0%" stop-color="rgba(240,208,96,.55)" />
                <stop offset="100%" stop-color="rgba(200,168,72,0)" />
              </radialGradient>
              <clipPath id="bowlInner">
                <path d="M24,20 Q24,10 60,10 Q96,10 96,20 L100,88 Q100,100 60,100 Q20,100 20,88 Z"/>
              </clipPath>
              <filter id="chaliceGlowF">
                <feGaussianBlur stdDeviation="2" result="blur"/>
                <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
              </filter>
            </defs>

            <!-- Back glow -->
            <ellipse cx="60" cy="55" rx="35" ry="18" fill="url(#liqGlow)" opacity=".4" class="chalice-glow" />

            <!-- ============ HANDLES ============ -->
            <path d="M24,40 Q6,40 6,60 Q6,75 20,75" fill="none" stroke="url(#goldTrim)" stroke-width="2.5" stroke-linecap="round" class="handle-left"/>
            <path d="M96,40 Q114,40 114,60 Q114,75 100,75" fill="none" stroke="url(#goldTrim)" stroke-width="2.5" stroke-linecap="round" class="handle-right"/>
            <!-- Handle gemstones -->
            <circle cx="6" cy="60" r="2.5" fill="#f05050" opacity=".7" />
            <circle cx="114" cy="60" r="2.5" fill="#f05050" opacity=".7" />

            <!-- ============ BOWL ============ -->
            <!-- Bowl back edge (rim underside) -->
            <path d="M28,18 Q28,10 60,10 Q92,10 92,18 L94,86 Q94,98 60,98 Q26,98 26,86 Z"
              fill="rgba(15,10,35,.4)" stroke="url(#glassGradC)" stroke-width="2"/>

            <!-- Arcane engraving on bowl -->
            <path d="M38,40 Q60,32 82,40" fill="none" stroke="rgba(200,168,72,.12)" stroke-width="1"/>
            <path d="M34,55 Q60,47 86,55" fill="none" stroke="rgba(200,168,72,.1)" stroke-width="1"/>
            <path d="M30,70 Q60,62 90,70" fill="none" stroke="rgba(200,168,72,.08)" stroke-width="1"/>
            <!-- Engraving rune dots -->
            <circle cx="60" cy="36" r="1.5" fill="rgba(200,168,72,.15)" />
            <circle cx="60" cy="51" r="1.5" fill="rgba(200,168,72,.12)" />
            <circle cx="60" cy="66" r="1.5" fill="rgba(200,168,72,.1)" />

            <!-- ============ LIQUID ============ -->
            <g clip-path="url(#bowlInner)">
              <path :d="`M20,${liquidY} L100,${liquidY} L100,105 L20,105 Z`" fill="url(#liquidGrad)" opacity=".85" class="liquid-fill"/>
              <!-- Liquid inner glow -->
              <ellipse v-if="store.progress > 0.05" :cx="60" :cy="liquidY + 4" rx="20" ry="4" fill="rgba(255,240,180,.25)"/>
            </g>

            <!-- Liquid surface -->
            <ellipse v-if="store.progress > 0"
              :cx="60" :cy="liquidY" :rx="40 - 40 * (liquidY - 16) / 72 + 16" ry="3.5"
              fill="rgba(252,240,160,.65)" class="liquid-surface" />
            <!-- Surface highlight -->
            <ellipse v-if="store.progress > 0.1"
              :cx="55" :cy="liquidY" :rx="12 - 12 * (liquidY - 16) / 72 + 6" ry="1.5"
              fill="rgba(255,255,255,.25)" class="liquid-surface" />

            <!-- Liquid bubbles -->
            <circle v-if="store.progress > 0.2" cx="50" cy="80" r="2" fill="none" stroke="rgba(255,255,255,.2)" stroke-width=".5" class="bubble b1"/>
            <circle v-if="store.progress > 0.35" cx="65" cy="70" r="1.5" fill="none" stroke="rgba(255,255,255,.15)" stroke-width=".5" class="bubble b2"/>
            <circle v-if="store.progress > 0.5" cx="45" cy="55" r="1.8" fill="none" stroke="rgba(255,255,255,.15)" stroke-width=".5" class="bubble b3"/>

            <!-- ============ RIM ============ -->
            <ellipse cx="60" cy="18" rx="36" ry="7" fill="url(#goldTrim)" opacity=".7"/>
            <ellipse cx="60" cy="18" rx="36" ry="7" fill="none" stroke="url(#goldTrim)" stroke-width="1.5"/>
            <!-- Rim gemstones -->
            <circle cx="38" cy="16.5" r="2.5" fill="#60b0f0" opacity=".6" />
            <circle cx="60" cy="15" r="3" fill="#f05050" opacity=".7" />
            <circle cx="82" cy="16.5" r="2.5" fill="#60b0f0" opacity=".6" />
            <!-- Rim highlight -->
            <ellipse cx="60" cy="17" rx="33" ry="5.5" fill="none" stroke="rgba(255,255,255,.2)" stroke-width=".8"/>

            <!-- ============ GLASS REFLECTIONS ============ -->
            <path d="M36,32 Q32,55 34,82" fill="none" stroke="rgba(255,255,255,.1)" stroke-width="1.8"/>
            <path d="M33,35 Q29,55 31,80" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="1"/>

            <!-- ============ STEAM ============ -->
            <g v-if="store.running" class="steam-group">
              <path d="M48,14 Q44,0 50,-12" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="1.8" class="steam s1"/>
              <path d="M60,12 Q56,-4 62,-16" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="1.5" class="steam s2"/>
              <path d="M72,14 Q76,0 70,-12" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="1.8" class="steam s3"/>
            </g>

            <!-- ============ NECK / COLLAR ============ -->
            <path d="M42,100 L42,96 Q42,102 60,102 Q78,102 78,96 L78,100 Z" fill="url(#goldTrim)" opacity=".5"/>
            <!-- Neck ring -->
            <ellipse cx="60" cy="100" rx="18" ry="3" fill="none" stroke="url(#goldTrim)" stroke-width="1.5"/>

            <!-- ============ STEM ============ -->
            <rect x="52" y="102" width="16" height="14" rx="2" fill="url(#glassGradC)" stroke="rgba(200,180,255,.12)" stroke-width="1"/>
            <!-- Stem decorative rings -->
            <ellipse cx="60" cy="105" rx="10" ry="2.5" fill="none" stroke="url(#goldTrim)" stroke-width="1"/>
            <ellipse cx="60" cy="113" rx="10" ry="2.5" fill="none" stroke="url(#goldTrim)" stroke-width="1"/>
            <!-- Stem knot/gem -->
            <ellipse cx="60" cy="119" rx="9" ry="3.5" fill="rgba(200,168,72,.15)" stroke="url(#goldTrim)" stroke-width="1.2"/>
            <ellipse cx="60" cy="119" rx="4" ry="1.8" fill="#f8d060" filter="url(#chaliceGlowF)"/>

            <!-- Lower stem -->
            <rect x="53" y="123" width="14" height="10" rx="2" fill="url(#glassGradC)" stroke="rgba(200,180,255,.1)" stroke-width="1"/>
            <!-- Lower ring -->
            <ellipse cx="60" cy="130" rx="9" ry="2" fill="none" stroke="url(#goldTrim)" stroke-width="1"/>

            <!-- ============ BASE ============ -->
            <!-- Base pedestal layers -->
            <ellipse cx="60" cy="136" rx="22" ry="4.5" fill="rgba(25,15,45,.45)" stroke="rgba(200,180,255,.18)" stroke-width="1.2"/>
            <ellipse cx="60" cy="138" rx="26" ry="4" fill="rgba(25,15,45,.55)" stroke="url(#goldTrim)" stroke-width="1.5" opacity=".6"/>
            <ellipse cx="60" cy="140" rx="30" ry="3.5" fill="rgba(20,12,35,.7)" stroke="url(#goldTrim)" stroke-width="1.8" opacity=".5"/>
            <!-- Base bottom plate -->
            <ellipse cx="60" cy="142" rx="32" ry="3" fill="rgba(15,8,25,.8)" stroke="rgba(200,180,255,.2)" stroke-width="1"/>
            <!-- Base gold rim -->
            <ellipse cx="60" cy="142" rx="32" ry="3" fill="none" stroke="url(#goldTrim)" stroke-width="2" opacity=".6"/>
            <!-- Base gemstones -->
            <circle cx="42" cy="141" r="1.8" fill="#60b0f0" opacity=".5"/>
            <circle cx="78" cy="141" r="1.8" fill="#60b0f0" opacity=".5"/>
          </svg>
        </div>

        <!-- Progress ring on the bowl -->
        <svg v-if="store.running" class="progress-ring" viewBox="0 0 100 100" width="110" height="110">
          <circle cx="50" cy="50" r="44" fill="none" stroke="rgba(200,168,72,.08)" stroke-width="2"/>
          <circle cx="50" cy="50" r="44" fill="none" stroke="#e8c860" stroke-width="2.5"
            stroke-dasharray="276.5" :stroke-dashoffset="276.5 * (1 - store.progress)"
            stroke-linecap="round" transform="rotate(-90 50 50)"/>
        </svg>
      </div>

      <!-- Quote text -->
      <div class="quote-text" v-if="store.running">{{ quote }}</div>

      <!-- Timer display -->
      <div class="timer-display">
        <span class="digit">{{ store.mm[0] }}</span><span class="digit">{{ store.mm[1] }}</span>
        <span class="timer-colon">:</span>
        <span class="digit">{{ store.ss[0] }}</span><span class="digit">{{ store.ss[1] }}</span>
      </div>

      <!-- Presets -->
      <div class="presets" v-if="!store.running && !store.done">
        <button v-for="m in presets" :key="m" :class="['preset-btn', { active: selected === m }]" @click="selected = m">
          {{ m }} 分钟
        </button>
      </div>

      <!-- Action buttons -->
      <div class="action-row" v-if="!store.running && !store.done">
        <button class="start-btn" @click="start">⚡ 开始专注</button>
      </div>
      <div class="action-row" v-if="store.running">
        <button class="abort-btn" @click="store.abort(); emit('close')">放弃专注</button>
      </div>

      <!-- Completion -->
      <div v-if="store.done" class="reward-pop">
        <div class="particle-burst">
          <span v-for="p in particles" :key="p.id" class="gold-particle" :style="{
            '--x': p.x + 'px', '--y': p.y + 'px', '--w': p.s + 'px', '--h': p.s + 'px',
            animationDelay: Math.random() * .3 + 's', animationDuration: p.d + 's'
          }"></span>
        </div>
        <div class="reward-icon">🏆</div>
        <div class="reward-text">专注完成！</div>
        <div class="reward-gold">+{{ store.reward }} 金币</div>
        <button class="reward-ok" @click="store.close(); emit('close')">收下奖励</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.focus-overlay { position:fixed; inset:0; z-index:300; display:flex; align-items:center; justify-content:center;
  background:rgba(3,3,16,.96); backdrop-filter:blur(20px); overflow:hidden; }

.starfield { position:absolute; inset:0; }
.star-dot { position:absolute; border-radius:50%; background:#fff;
  animation: twinkle 2s ease-in-out infinite; }
@keyframes twinkle { 0%,100%{opacity:.1} 50%{opacity:.6} }

.aura-glow { position:absolute; width:420px; height:420px; border-radius:50%;
  background:radial-gradient(circle, rgba(120,80,200,.06) 0%, transparent 70%);
  transition:all 1.5s ease; }
.aura-glow.breathing { animation: breathe 4s ease-in-out infinite; }
.aura-glow.active { width:520px; height:520px; background:radial-gradient(circle, rgba(200,168,72,.08) 0%, transparent 70%);
  animation: breatheActive 3s ease-in-out infinite; }
@keyframes breathe { 0%,100%{transform:scale(1);opacity:.6} 50%{transform:scale(1.3);opacity:1} }
@keyframes breatheActive { 0%,100%{transform:scale(1);opacity:.5} 50%{transform:scale(1.15);opacity:1} }

.focus-panel { position:relative; display:flex; flex-direction:column; align-items:center; gap:14px; padding:32px 44px;
  background:radial-gradient(ellipse at center, rgba(30,15,50,.7) 0%, rgba(8,4,20,.85) 100%);
  border:1px solid rgba(180,160,240,.12); border-radius:20px; z-index:1;
  box-shadow:0 0 60px rgba(100,60,180,.1), 0 0 160px rgba(80,40,140,.06), inset 0 1px 0 rgba(255,255,255,.03); }

.focus-close { position:absolute; top:14px; right:18px; background:none; border:none; color:rgba(255,255,255,.25); font-size:22px; cursor:pointer; transition:color .2s; z-index:2; }
.focus-close:hover { color:rgba(255,255,255,.6); }

/* Chalice + Rune Rings */
.chalice-wrap { position:relative; width:200px; height:200px; display:flex; align-items:center; justify-content:center; }

.rune-ring { position:absolute; inset:0; margin:auto; }
.ring-a { animation: spinRuneA 30s linear infinite; }
.ring-b { animation: spinRuneB 20s linear infinite; }
.ring-c { animation: spinRuneC 15s linear infinite; }
@keyframes spinRuneA { to { transform:rotate(360deg); } }
@keyframes spinRuneB { to { transform:rotate(-360deg); } }
@keyframes spinRuneC { to { transform:rotate(360deg); } }
.rune-char { font-family:serif; }

.chalice-svg { position:relative; z-index:1; filter:drop-shadow(0 0 20px rgba(200,168,72,.25)); }

.chalice-glow { animation: glowPulse 2s ease-in-out infinite; }
@keyframes glowPulse { 0%,100%{opacity:.25} 50%{opacity:.55} }

.liquid-fill { transition: d .5s ease; }

.liquid-surface { animation: surfShimmer 1.5s ease-in-out infinite; }
@keyframes surfShimmer { 0%,100%{opacity:.4} 50%{opacity:.85} }

.bubble { animation: bubbleUp 2s ease-in-out infinite; }
.b1 { animation-delay: 0s; }
.b2 { animation-delay: .7s; }
.b3 { animation-delay: 1.3s; }
@keyframes bubbleUp { 0%,100%{opacity:0; transform:translateY(0)} 30%{opacity:.6} 60%{opacity:.4; transform:translateY(-8px)} 100%{opacity:0; transform:translateY(-16px)} }

.steam { animation: steamRise 2s ease-out infinite; }
.s1 { animation-delay: 0s; }
.s2 { animation-delay: .7s; }
.s3 { animation-delay: 1.4s; }
@keyframes steamRise {
  0%{opacity:0; transform:translateY(0) scale(1)}
  20%{opacity:.4}
  100%{opacity:0; transform:translateY(-16px) scale(1.8)}
}

.progress-ring { position:absolute; }
.progress-ring circle { transition: stroke-dashoffset .3s linear; }

/* Quote */
.quote-text { font-family:'Cormorant Garamond','Noto Serif SC',serif; font-size:14px; color:rgba(200,168,72,.4); font-style:italic; text-align:center; max-width:260px; letter-spacing:1px; }

/* Timer */
.timer-display { display:flex; align-items:center; gap:2px; font-family:'Cinzel',serif; font-weight:700; }
.digit { display:inline-flex; align-items:center; justify-content:center; width:40px; height:60px;
  font-size:52px; color:#e8c860;
  background:rgba(0,0,0,.2); border:1px solid rgba(200,168,72,.1); border-radius:6px;
  text-shadow:0 0 16px rgba(232,200,96,.5), 0 0 32px rgba(232,168,64,.25); }
.timer-colon { font-size:36px; color:rgba(200,168,72,.3); margin:0 2px; animation: colonBlink .8s ease-in-out infinite; }
@keyframes colonBlink { 50% { opacity: .15; } }

/* Presets */
.presets { display:flex; gap:8px; }
.preset-btn { padding:8px 20px; border:1px solid rgba(180,160,240,.12); border-radius:10px; background:rgba(255,255,255,.02); color:rgba(220,210,240,.4); cursor:pointer; font-family:'Cinzel',serif; font-size:13px; transition:all .2s; }
.preset-btn:hover { border-color:rgba(200,180,255,.25); color:rgba(220,210,240,.7); }
.preset-btn.active { border-color:#c9a84c; background:rgba(200,168,72,.08); color:#e8c860; box-shadow:0 0 18px rgba(200,168,72,.1); }

/* Buttons */
.action-row { display:flex; gap:12px; }
.start-btn { padding:12px 40px; border:none; border-radius:12px;
  background:linear-gradient(135deg, #b09030, #c9a84c, #d4b860); color:#1a1008; cursor:pointer;
  font-family:'Cinzel',serif; font-size:16px; font-weight:700; letter-spacing:3px;
  transition:all .25s; position:relative; overflow:hidden; }
.start-btn::after { content:''; position:absolute; inset:0; background:linear-gradient(135deg, transparent 40%, rgba(255,255,255,.15) 50%, transparent 60%); transform:translateX(-100%); transition:transform .4s; }
.start-btn:hover::after { transform:translateX(100%); }
.start-btn:hover { transform:scale(1.05); box-shadow:0 0 30px rgba(200,168,72,.3), 0 0 60px rgba(200,168,72,.1); }

.abort-btn { padding:9px 24px; border:1px solid rgba(200,100,100,.15); border-radius:10px; background:rgba(200,80,80,.04); color:rgba(200,140,140,.5); cursor:pointer; font-size:13px; transition:all .2s; }
.abort-btn:hover { background:rgba(200,80,80,.08); border-color:rgba(200,100,100,.3); color:rgba(200,140,140,.8); }

/* Completion */
.reward-pop { display:flex; flex-direction:column; align-items:center; gap:8px; position:relative; padding:10px 0; overflow:visible; }
.particle-burst { position:absolute; inset:0; pointer-events:none; }
.gold-particle { position:absolute; left:50%; top:50%; border-radius:50%; background:#f0d060;
  width:var(--w); height:var(--h);
  animation: burstOut var(--d) ease-out forwards;
  box-shadow:0 0 6px rgba(240,208,96,.6); }
@keyframes burstOut {
  0%{transform:translate(0,0) scale(1);opacity:1}
  100%{transform:translate(var(--x),var(--y)) scale(0);opacity:0}
}
.reward-icon { font-size:44px; animation: bounce 1s ease-in-out infinite; }
@keyframes bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.reward-text { font-family:'Cinzel',serif; font-size:20px; color:#e8c860; letter-spacing:3px; }
.reward-gold { font-size:26px; color:#f0d060; font-weight:bold; text-shadow:0 0 16px rgba(240,208,96,.5), 0 0 36px rgba(240,200,80,.2); }
.reward-ok { margin-top:6px; padding:10px 36px; border:1px solid rgba(200,168,72,.25); border-radius:10px; background:rgba(200,168,72,.12); color:#e8c860; cursor:pointer; font-family:'Cinzel',serif; font-size:14px; transition:all .2s; }
.reward-ok:hover { background:rgba(200,168,72,.25); border-color:rgba(200,168,72,.4); transform:scale(1.04); }
</style>
