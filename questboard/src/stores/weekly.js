import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useQuestStore } from './quest.js'

const DIFF_REWARDS = { '普通': 20, '困难': 50, '史诗': 100 }

export const useWeeklyStore = defineStore('weekly', () => {
  const lastShown = ref(localStorage.getItem('weekly_last_shown') || '')
  const showReport = ref(false)
  const report = ref(null)

  function getMonday(offset = 0) {
    const now = new Date()
    const d = new Date(now)
    d.setDate(d.getDate() - ((d.getDay() || 7) - 1) - offset * 7)
    d.setHours(0, 0, 0, 0)
    return d
  }

  function computeReport() {
    const qs = useQuestStore()
    const monday = getMonday()
    const lastMonday = getMonday(1)

    const thisWeek = qs.tasks.filter(t => {
      const d = new Date(t.created_at || t.date)
      return d >= monday && t.completed
    })
    const lastWeek = qs.tasks.filter(t => {
      const d = new Date(t.created_at || t.date)
      return d >= lastMonday && d < monday && t.completed
    })

    const gold = thisWeek.reduce((s, t) => s + (DIFF_REWARDS[t.difficulty] || 20), 0)
    const lastGold = lastWeek.reduce((s, t) => s + (DIFF_REWARDS[t.difficulty] || 20), 0)

    const clients = {}
    thisWeek.forEach(t => {
      const c = t.client || '村庄长老'
      clients[c] = (clients[c] || 0) + 1
    })
    const topClient = Object.entries(clients).sort((a, b) => b[1] - a[1])[0] || ['无', 0]

    report.value = {
      total: thisWeek.length,
      lastTotal: lastWeek.length,
      gold,
      lastGold,
      epic: thisWeek.filter(t => t.difficulty === '史诗').length,
      topClient: topClient[0],
      topCount: topClient[1],
      weekNum: Math.ceil((new Date() - new Date(new Date().getFullYear(), 0, 1)) / 604800000),
    }
    return report.value
  }

  function checkShow() {
    if (showReport.value) return false
    const now = new Date()
    const today = now.toISOString().slice(0, 10)
    if (lastShown.value === today) return false
    lastShown.value = today
    localStorage.setItem('weekly_last_shown', today)
    computeReport()
    showReport.value = true
    return true
  }

  function close() {
    showReport.value = false
  }

  return { showReport, report, checkShow, close, computeReport }
})
