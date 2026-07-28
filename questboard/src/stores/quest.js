import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAudioStore } from './audio.js'

const isElectron = typeof window !== 'undefined' && window.api

async function loadJson(filename, fallback) {
  const local = localStorage.getItem(filename)
  if (local) { try { return JSON.parse(local) } catch {} }
  if (isElectron) return await window.api.readJson(filename) || fallback
  return fallback
}
async function saveJson(filename, data) {
  localStorage.setItem(filename, JSON.stringify(data))
  if (isElectron) { try { await window.api.writeJson(filename, data) } catch {} }
}
async function saveSyncJson(filename, data) {
  localStorage.setItem(filename, JSON.stringify(data))
}

export const useQuestStore = defineStore('quest', () => {
  const tasks = ref([])
  const hero = ref({ name: '勇者', level: 1, exp: 0, hp: 100, maxHp: 100, gold: 0, streak: 0, last_login: '' })
  const aiSettings = ref({ enabled: false, api_key: '', api_base: 'https://api.deepseek.com', model: 'deepseek-v4-flash', system_prompt: '' })
  const showVictory = ref(false)
  const lastCompleted = ref(null)
  const loaded = ref(false)
  const converting = ref(false)

  const activeTasks = computed(() => tasks.value.filter(t => !t.completed))
  const completedTasks = computed(() => tasks.value.filter(t => t.completed))
  const futureTasks = computed(() => {
    const qt = questToday()
    return tasks.value.filter(t => !t.completed && t.date > qt)
  })
  const gold = computed(() => hero.value.gold)
  const epicCount = computed(() => completedTasks.value.filter(t => t.difficulty === '史诗').length)
  const aiEnabled = computed({
    get: () => aiSettings.value.enabled,
    set: (v) => { aiSettings.value.enabled = v; persistAi() }
  })

  async function load() {
    tasks.value = await loadJson('tasks.json', [])
    tasks.value = tasks.value.filter(t => t.name && t.name.trim())
    hero.value = await loadJson('hero.json', { name: '勇者', level: 1, exp: 0, hp: 100, maxHp: 100, gold: 0, streak: 0, last_login: '' })
    await loadAi()
    loaded.value = true
    // Auto-save on close
    window.addEventListener('beforeunload', () => saveSync())
  }

  function saveSync() {
    const data = JSON.parse(JSON.stringify(tasks.value))
    const heroData = JSON.parse(JSON.stringify(hero.value))
    localStorage.setItem('tasks.json', JSON.stringify(data))
    localStorage.setItem('hero.json', JSON.stringify(heroData))
  }

  async function loadAi() {
    const s = await loadJson('ai_settings.json', null)
    if (s) aiSettings.value = s
  }
  async function persistAi() { await saveJson('ai_settings.json', aiSettings.value) }

  async function save() {
    localStorage.setItem('tasks.json', JSON.stringify(tasks.value))
    localStorage.setItem('hero.json', JSON.stringify(hero.value))
    if (isElectron) {
      try { await window.api.writeJson('tasks.json', tasks.value) } catch {}
      try { await window.api.writeJson('hero.json', hero.value) } catch {}
    }
  }

  async function convertTask(text) {
    const key = aiSettings.value.api_key?.trim()
    if (!key || !aiSettings.value.enabled) return null
    converting.value = true
    try {
      const base = (aiSettings.value.api_base || 'https://api.deepseek.com').replace(/\/+$/, '')
      const resp = await fetch(`${base}/chat/completions`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: aiSettings.value.model || 'deepseek-chat',
          messages: [
            { role: 'system', content: aiSettings.value.system_prompt || '把待办转成奇幻冒险任务，15字以内，只输出任务名' },
            { role: 'user', content: `请把这个待办转为悬赏任务名：${text}` },
          ],
          max_tokens: 200, temperature: 0.8,
        }),
      })
      const data = await resp.json()
      let content = data.choices?.[0]?.message?.content?.trim() || ''
      content = content.replace(/^["'`「」『』]|["'`「」『』]$/g, '').slice(0, 25)
      return content || null
    } catch (e) {
      console.error('[AI]', e)
      return null
    } finally {
      converting.value = false
    }
  }

  async function addTask(task) {
    tasks.value.push({
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
      name: task.title,
      original_name: task.original_name || null,
      difficulty: task.difficulty,
      date: task.date || questToday(),
      completed: false,
      created_at: new Date().toISOString(),
    })
    useAudioStore().play('post')
    await save()
    try { (await import('./achievements.js')).useAchievementsStore().checkAll() } catch {}
  }

  const DIFF_REWARDS = { '普通': 20, '困难': 50, '史诗': 100 }

  async function completeTask(id) {
    const t = tasks.value.find(x => x.id === id)
    if (!t) return
    t.completed = true
    const r = DIFF_REWARDS[t.difficulty] || 20
    hero.value.gold += r
    hero.value.exp += r
    const oldLevel = hero.value.level
    while (hero.value.exp >= hero.value.level * 100) {
      hero.value.exp -= hero.value.level * 100; hero.value.level++
      hero.value.maxHp += 10; hero.value.hp = Math.min(hero.value.hp + 20, hero.value.maxHp)
    }
    const audio = useAudioStore()
    if (hero.value.level > oldLevel) audio.play('levelup')
    else audio.play('complete')
    const td = tasks.value.filter(x => x.date === questToday() && !x.completed)
    if (td.length === 0) {
      hero.value.streak++
      const bonus = Math.floor(tasks.value.filter(x => x.date === questToday()).reduce((s, x) => s + (DIFF_REWARDS[x.difficulty] || 20), 0) * 0.2)
      hero.value.gold += bonus; hero.value.exp += bonus
      useAudioStore().play('allclear')
    }
    lastCompleted.value = t; showVictory.value = true
    await save()
    try { (await import('./achievements.js')).useAchievementsStore().checkAll() } catch {}
  }

  async function deleteTask(id) { tasks.value = tasks.value.filter(x => x.id !== id); useAudioStore().play('delete'); await save() }
  function closeVictory() { showVictory.value = false }

  function questToday() {
    const now = new Date()
    if (now.getHours() < 8) now.setDate(now.getDate() - 1)
    return now.toISOString().slice(0, 10)
  }

  return { tasks, hero, aiSettings, aiEnabled, gold, epicCount, showVictory, lastCompleted, loaded, converting,
           activeTasks, completedTasks, futureTasks, load, loadAi, persistAi, convertTask, addTask, completeTask, deleteTask, closeVictory, questToday }
})
