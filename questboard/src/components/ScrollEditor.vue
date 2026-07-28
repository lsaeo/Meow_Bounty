<script setup>
import { ref } from 'vue'
import { useQuestStore } from '../stores/quest.js'
import gsap from 'gsap'

const store = useQuestStore()
const emit = defineEmits(['close'])
const title = ref('')
const difficulty = ref('普通')
const client = ref('村庄长老')
const scheduleDate = ref(store.questToday())
const showAiSettings = ref(false)
const aiKey = ref(''); const aiBase = ref(''); const aiModel = ref(''); const aiPrompt = ref('')

const difficulties = [
  { name: '普通', color: '#5ad8a0', icon: '◆', reward: 20, glow: 'rgba(90,216,160,.4)' },
  { name: '困难', color: '#e8c050', icon: '★', reward: 50, glow: 'rgba(232,192,80,.4)' },
  { name: '史诗', color: '#c0a0f0', icon: '▲', reward: 100, glow: 'rgba(192,160,240,.4)' },
]
const clients = ['村庄长老', '法师塔', '佣兵工会', '铁匠铺', '旅店', '精灵信使']

function setToday() { scheduleDate.value = store.questToday() }
function tomorrowDate() {
  const dt = new Date(store.questToday())
  dt.setDate(dt.getDate() + 1)
  return dt.toISOString().slice(0, 10)
}
function setTomorrow() { scheduleDate.value = tomorrowDate() }

function openAiSettings() {
  aiKey.value = store.aiSettings.api_key || ''
  aiBase.value = store.aiSettings.api_base || 'https://api.deepseek.com'
  aiModel.value = store.aiSettings.model || 'deepseek-v4-flash'
  aiPrompt.value = store.aiSettings.system_prompt || '你是冒险者公会的长老，负责将村民们的日常委托转化为中世纪奇幻风格的悬赏任务。\n规则：1) 保留原任务的核心含义，但用奇幻世界观重写；2) 控制在15字以内；3) 使用类似"讨伐""寻找""锻造""破译""护送"等动作词；4) 加入怪物、魔法、异世界元素；5) 只输出任务名，不要解释。\n\n世界观：剑与魔法世界，有龙族、哥布林、精灵、矮人、不死族等种族。'
  showAiSettings.value = true
}
function saveAiSettings() {
  store.aiSettings.api_key = aiKey.value.trim()
  store.aiSettings.api_base = aiBase.value.trim() || 'https://api.deepseek.com'
  store.aiSettings.model = aiModel.value.trim() || 'deepseek-v4-flash'
  store.aiSettings.system_prompt = aiPrompt.value.trim()
  store.persistAi()
  showAiSettings.value = false
}

async function submit() {
  if (!title.value.trim()) return
  const original = title.value.trim()
  let finalTitle = original, originalName = null
  if (store.aiEnabled) { 
    const converted = await store.convertTask(original)
    finalTitle = (converted && converted.trim()) || original
    originalName = finalTitle !== original ? original : null 
  }
  const d = difficulties.find(x => x.name === difficulty.value)
  store.addTask({ title: finalTitle, original_name: originalName, difficulty: difficulty.value, reward: d.reward, client: client.value, date: scheduleDate.value })
  title.value = ''
  gsap.to('.wax-seal', { scale: 1.3, duration: .2, yoyo: true, repeat: 1, onComplete: () => emit('close') })
}
</script>

<template>
  <div class="scroll-overlay" @click.self="emit('close')">
    <div class="scroll-paper">
      <div class="scroll-rod top-rod"></div>
      <div class="scroll-content" v-if="!showAiSettings">
        <h2 class="scroll-title">📜 张贴悬赏令</h2>
        <textarea v-model="title" placeholder="在此写下悬赏内容..." class="quest-input" rows="3" />
        <div class="diff-chooser">
          <button v-for="d in difficulties" :key="d.name" :class="['diff-btn', { active: difficulty === d.name }]"
                  :style="{ borderColor: d.color, boxShadow: difficulty===d.name ? `0 0 16px ${d.glow}` : '' }" @click="difficulty = d.name">
            <span class="diff-icon" :style="{ color: d.color }">{{ d.icon }}</span>
            <span>{{ d.name }}</span>
            <small>{{ d.reward }}金币</small>
          </button>
        </div>
        <label class="field-label">委托人</label>
        <select v-model="client" class="client-select">
          <option v-for="c in clients" :key="c" :value="c">{{ c }}</option>
        </select>
        <label class="field-label">排期日期</label>
        <div class="date-row">
          <input type="date" v-model="scheduleDate" class="date-input" />
          <span class="date-quick" :class="{ active: scheduleDate===store.questToday() }" @click="setToday">今天</span>
          <span class="date-quick" :class="{ active: scheduleDate===tomorrowDate() }" @click="setTomorrow">明天</span>
        </div>
        <div class="ai-row">
          <label class="ai-toggle"><input type="checkbox" v-model="store.aiEnabled" /> AI 转化</label>
          <span class="ai-gear" @click="openAiSettings">⚙</span>
          <small v-if="store.converting" class="ai-converting">转化中...</small>
        </div>
        <div class="wax-seal" @click="submit">
          <svg width="56" height="56" viewBox="0 0 56 56">
            <circle cx="28" cy="28" r="26" fill="#8b2020" stroke="#5a1010" stroke-width="2"/>
            <circle cx="28" cy="28" r="18" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="1"/>
            <line x1="16" y1="28" x2="40" y2="28" stroke="rgba(255,255,255,.35)" stroke-width="2"/>
            <line x1="28" y1="16" x2="28" y2="40" stroke="rgba(255,255,255,.35)" stroke-width="2"/>
          </svg>
          <span class="seal-label">张贴</span>
        </div>
      </div>
      <!-- AI Settings -->
      <div class="scroll-content" v-else>
        <h2 class="scroll-title">⚙ AI 设置</h2>
        <input v-model="aiKey" placeholder="API Key" class="ai-field" type="password" />
        <input v-model="aiBase" placeholder="API Base URL" class="ai-field" />
        <input v-model="aiModel" placeholder="Model" class="ai-field" />
        <textarea v-model="aiPrompt" placeholder="系统提示词" class="ai-field ai-textarea" rows="4"></textarea>
        <div class="ai-settings-btns">
          <button @click="saveAiSettings" class="ai-save-btn">保存</button>
          <button @click="showAiSettings = false" class="ai-cancel-btn">返回</button>
        </div>
      </div>
      <div class="scroll-rod bottom-rod"></div>
    </div>
  </div>
</template>

<style scoped>
.scroll-overlay { position: fixed; inset: 0; z-index: 200; background: rgba(0,0,0,.75); display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); }
.scroll-paper { width: 480px; max-height: 80vh; background: linear-gradient(180deg, #1e1830 0%, #181428 50%, #141024 100%); border: 1px solid rgba(200,168,72,.3); border-radius: 6px; box-shadow: 0 0 60px rgba(110,142,240,.1), 0 8px 40px rgba(0,0,0,.6); display: flex; flex-direction: column; }
.scroll-rod { height: 6px; background: linear-gradient(180deg, var(--gold-dim), #3e2216, var(--gold-dim)); border-radius: 3px; }
.scroll-content { padding: 20px 28px; }
.scroll-title { font-family: 'Cinzel', serif; font-size: 20px; color: var(--gold-bright); text-align: center; margin-bottom: 16px; letter-spacing: 2px; }
.quest-input { width: 100%; background: rgba(255,255,255,.12); border: 2px solid rgba(200,168,72,.3); border-radius: 6px; font-family: 'Cormorant Garamond', 'Noto Serif SC', serif; font-size: 17px; color: #e8d8b8; padding: 12px 14px; resize: none; outline: none; }
.quest-input:focus { border-color: var(--gold); background: rgba(255,255,255,.18); }
.quest-input::placeholder { color: rgba(200,170,140,.4); }
.diff-chooser { display: flex; gap: 8px; margin: 14px 0; }
.diff-btn { flex: 1; padding: 10px 6px; border: 1px solid rgba(255,255,255,.12); border-radius: 8px; background: rgba(255,255,255,.04); cursor: pointer; text-align: center; transition: all .2s; color: rgba(200,180,160,.5); font-size: 13px; }
.diff-btn.active { background: rgba(255,255,255,.1); border-color: var(--gold); color: #e8d8b8; transform: scale(1.03); }
.diff-icon { font-size: 18px; display: block; margin-bottom: 2px; }
.diff-btn small { color: var(--gold-dim); font-size: 10px; display: block; margin-top: 2px; }
.field-label { display: block; font-family: 'Cinzel', serif; font-size: 12px; color: rgba(200,168,72,.5); margin-bottom: 4px; }
.client-select { width: 100%; padding: 8px 10px; border: 1px solid rgba(200,168,72,.2); border-radius: 6px; background: rgba(255,255,255,.08); color: #e8d8b8; font-size: 14px; margin-bottom: 12px; }
.client-select option { background: #1e1830; color: #e8d8b8; }
.date-input { flex:1; padding:8px 10px; border:1px solid rgba(200,168,72,.2); border-radius:6px; background:rgba(255,255,255,.08); color:#e8d8b8; font-size:14px; }
.date-input::-webkit-calendar-picker-indicator { filter: invert(.8); }
.date-row { display:flex; gap:6px; align-items:center; margin-bottom:10px; }
.date-row .date-input { margin-bottom:0; flex:1; }
.date-quick { padding:5px 10px; border:1px solid rgba(200,168,72,.15); border-radius:4px; cursor:pointer; font-size:11px; color:var(--gold-dim); transition:all .15s; white-space:nowrap; user-select:none; }
.date-quick:hover { background:rgba(200,168,72,.1); color:var(--gold-bright); }
.date-quick.active { background:var(--gold-dim); color:var(--oak-deep); border-color:var(--gold); transform:scale(.95); box-shadow:inset 0 2px 4px rgba(0,0,0,.3); }
.ai-row { display: flex; align-items: center; gap: 10px; margin: 10px 0; padding: 8px 12px; background: rgba(110,142,240,.06); border-radius: 6px; border: 1px solid rgba(110,142,240,.15); }
.ai-toggle { font-size: 13px; color: #c8b898; cursor: pointer; display: flex; align-items: center; gap: 6px; }
.ai-gear { cursor: pointer; font-size: 14px; color: var(--gold-dim); transition: color .2s; }
.ai-gear:hover { color: var(--gold); }
.ai-converting { color: #e8c860; font-size: 11px; animation: pulse .8s infinite; }
@keyframes pulse { 50% { opacity: .4; } }
.wax-seal { display: flex; flex-direction: column; align-items: center; cursor: pointer; margin-top: 14px; transition: filter .2s; }
.wax-seal:hover { filter: brightness(1.2); }
.seal-label { font-family: 'Cinzel', serif; font-size: 11px; color: #c08080; margin-top: 4px; }
.ai-field { width: 100%; padding: 8px 10px; border: 1px solid rgba(200,168,72,.2); border-radius: 6px; font-size: 13px; margin-bottom: 8px; background: rgba(255,255,255,.08); color: #e8d8b8; }
.ai-textarea { resize: none; }
.ai-settings-btns { display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px; }
.ai-save-btn, .ai-cancel-btn { padding: 7px 16px; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; font-family: 'Cinzel', serif; }
.ai-save-btn { background: linear-gradient(135deg, var(--success), #3a8a5a); color: #fff; }
.ai-cancel-btn { background: rgba(255,255,255,.08); color: #c8b898; border: 1px solid rgba(255,255,255,.1); }
</style>
