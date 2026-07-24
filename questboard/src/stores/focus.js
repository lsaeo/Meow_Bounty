import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useQuestStore } from './quest.js'
import { useAudioStore } from './audio.js'

export const useFocusStore = defineStore('focus', () => {
  const active = ref(false)
  const running = ref(false)
  const remaining = ref(0)
  const total = ref(0)
  const done = ref(false)
  let timer = null

  const reward = computed(() => Math.floor(total.value / 60) * 2)
  const progress = computed(() => total.value ? (total.value - remaining.value) / total.value : 0)
  const mm = computed(() => String(Math.floor(remaining.value / 60)).padStart(2, '0'))
  const ss = computed(() => String(remaining.value % 60).padStart(2, '0'))

  function start(minutes) {
    total.value = minutes * 60
    remaining.value = total.value
    done.value = false
    active.value = true
    running.value = true
    useAudioStore().play('click')
    timer = setInterval(tick, 1000)
  }

  function tick() {
    if (remaining.value <= 0) {
      abort()
      done.value = true
      const quest = useQuestStore()
      quest.hero.gold += reward.value
      useAudioStore().play('complete')
      try { quest.save() } catch {}
      return
    }
    remaining.value--
  }

  function abort() {
    if (timer) { clearInterval(timer); timer = null }
    running.value = false
  }

  function close() {
    abort()
    active.value = false
    remaining.value = 0
    done.value = false
  }

  return { active, running, remaining, total, done, reward, progress, mm, ss, start, abort, close }
})
