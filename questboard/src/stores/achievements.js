import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useQuestStore } from './quest.js'

const ACHIEVEMENTS = [
  // 新手系列
  { id: 'first_quest', name: '初出茅庐', desc: '完成第一个悬赏', icon: '⚔️', check: (s) => s.completedTasks.length >= 1 },
  { id: 'first_epic', name: '史诗初战', desc: '完成1个史诗悬赏', icon: '▲', check: (s) => s.completedTasks.filter(t => t.difficulty === '史诗').length >= 1 },
  { id: 'three_diff', name: '全能勇者', desc: '同时拥有普通、困难、史诗各一个', icon: '🎯', check: (s) => {
    const done = s.completedTasks; return ['普通','困难','史诗'].every(d => done.some(t => t.difficulty === d))
  }},
  // 连击系列
  { id: 'streak_3', name: '连续奋战', desc: '连续3天全清', icon: '🔥', check: (s) => (s.hero?.streak || 0) >= 3 },
  { id: 'streak_7', name: '全勤勇士', desc: '连续7天全清', icon: '⭐', check: (s) => (s.hero?.streak || 0) >= 7 },
  { id: 'streak_14', name: '钢铁意志', desc: '连续14天全清', icon: '💪', check: (s) => (s.hero?.streak || 0) >= 14 },
  { id: 'streak_30', name: '传说之证', desc: '连续30天全清', icon: '🏆', check: (s) => (s.hero?.streak || 0) >= 30 },
  // 史诗系列
  { id: 'epic_1', name: '史诗初战', desc: '完成1个史诗悬赏', icon: '▲', check: (s) => s.completedTasks.filter(t => t.difficulty === '史诗').length >= 1 },
  { id: 'epic_5', name: '史诗杀手', desc: '完成5个史诗悬赏', icon: '👑', check: (s) => s.completedTasks.filter(t => t.difficulty === '史诗').length >= 5 },
  { id: 'epic_10', name: '屠龙专家', desc: '完成10个史诗悬赏', icon: '🐉', check: (s) => s.completedTasks.filter(t => t.difficulty === '史诗').length >= 10 },
  // 金币系列
  { id: 'gold_100', name: '第一桶金', desc: '累计100金币', icon: '🪙', check: (s) => (s.hero?.gold || 0) >= 100 },
  { id: 'gold_500', name: '小有积蓄', desc: '累计500金币', icon: '💰', check: (s) => (s.hero?.gold || 0) >= 500 },
  { id: 'gold_1000', name: '赏金猎人', desc: '累计1000金币', icon: '💎', check: (s) => (s.hero?.gold || 0) >= 1000 },
  { id: 'gold_5000', name: '富可敌国', desc: '累计5000金币', icon: '🏦', check: (s) => (s.hero?.gold || 0) >= 5000 },
  // 数量系列
  { id: 'total_5', name: '初显身手', desc: '累计完成5个悬赏', icon: '📋', check: (s) => s.completedTasks.length >= 5 },
  { id: 'total_10', name: '冒险老手', desc: '累计完成10个悬赏', icon: '🛡️', check: (s) => s.completedTasks.length >= 10 },
  { id: 'total_20', name: '身经百战', desc: '累计完成20个悬赏', icon: '⚡', check: (s) => s.completedTasks.length >= 20 },
  { id: 'total_50', name: '百战英豪', desc: '累计完成50个悬赏', icon: '🎖️', check: (s) => s.completedTasks.length >= 50 },
  { id: 'total_100', name: '传奇勇者', desc: '累计完成100个悬赏', icon: '🌟', check: (s) => s.completedTasks.length >= 100 },
  // 一日系列
  { id: 'day_3', name: '一日三秋', desc: '一天内完成3个悬赏', icon: '⚡', check: (s) => {
    const today = new Date().toISOString().slice(0,10)
    return s.completedTasks.filter(t => t.created_at?.startsWith(today) || t.date === today).length >= 3
  }},
  { id: 'day_5', name: '超级工作日', desc: '一天内完成5个悬赏', icon: '🚀', check: (s) => {
    const today = new Date().toISOString().slice(0,10)
    return s.completedTasks.filter(t => t.created_at?.startsWith(today) || t.date === today).length >= 5
  }},
  // 升级系列
  { id: 'level_5', name: '见习骑士', desc: '达到Lv.5', icon: '⚜️', check: (s) => (s.hero?.level || 1) >= 5 },
  { id: 'level_10', name: '王国骑士', desc: '达到Lv.10', icon: '🏰', check: (s) => (s.hero?.level || 1) >= 10 },
  { id: 'level_20', name: '龙骑士', desc: '达到Lv.20', icon: '🐲', check: (s) => (s.hero?.level || 1) >= 20 },
]

export const useAchievementsStore = defineStore('achievements', () => {
  const unlocked = ref(JSON.parse(localStorage.getItem('achievements') || '[]'))
  const queue = ref([])
  const showing = ref(false)

  const allAchievements = computed(() => ACHIEVEMENTS)

  function isUnlocked(id) { return unlocked.value.includes(id) }

  function checkAll() {
    const qs = useQuestStore()
    for (const a of ACHIEVEMENTS) {
      if (unlocked.value.includes(a.id)) continue
      try {
        if (a.check(qs)) {
          unlock(a.id)
        }
      } catch(e) { console.log('ach check err', a.id, e) }
    }
  }

  function unlock(id) {
    if (unlocked.value.includes(id)) return
    unlocked.value.push(id)
    localStorage.setItem('achievements', JSON.stringify(unlocked.value))
    queue.value.push(id)
    if (!showing.value) showNext()
  }

  function showNext() {
    if (queue.value.length === 0) { showing.value = false; return }
    showing.value = true
  }

  function onPopupClosed() {
    queue.value.shift()
    showing.value = false
    if (queue.value.length > 0) {
      setTimeout(() => { showing.value = true }, 200)
    }
  }

  function currentAchievement() {
    if (queue.value.length === 0) return null
    return ACHIEVEMENTS.find(a => a.id === queue.value[0]) || null
  }

  return { unlocked, queue, showing, allAchievements, isUnlocked, checkAll, unlock, onPopupClosed, currentAchievement }
})
