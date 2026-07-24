import { defineStore } from 'pinia'
import { ref } from 'vue'

let audioCtx = null

function getCtx() {
  if (!audioCtx) {
    try { audioCtx = new (window.AudioContext || window.webkitAudioContext)() } catch { return null }
  }
  if (audioCtx.state === 'suspended') audioCtx.resume()
  return audioCtx
}

function playTone(freq, duration, type = 'sine', vol = 0.15) {
  const ctx = getCtx()
  if (!ctx) return
  const osc = ctx.createOscillator()
  const gain = ctx.createGain()
  osc.type = type
  osc.frequency.value = freq
  gain.gain.setValueAtTime(vol, ctx.currentTime)
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration)
  osc.connect(gain)
  gain.connect(ctx.destination)
  osc.start(ctx.currentTime)
  osc.stop(ctx.currentTime + duration)
}

// Synthesized sound effects
const SYNTHS = {
  complete: () => {
    playTone(800, 0.1, 'triangle', 0.12)
    setTimeout(() => playTone(1200, 0.12, 'triangle', 0.1), 80)
  },
  levelup: () => {
    [523, 659, 784, 1047].forEach((f, i) =>
      setTimeout(() => playTone(f, 0.2, 'triangle', 0.1), i * 120))
  },
  post: () => {
    playTone(400, 0.08, 'sine', 0.08)
    setTimeout(() => playTone(300, 0.06, 'sine', 0.06), 60)
  },
  allclear: () => {
    [523, 659, 784, 1047, 784, 1047].forEach((f, i) =>
      setTimeout(() => playTone(f, 0.25, 'triangle', 0.12), i * 150))
  },
  delete: () => {
    playTone(300, 0.08, 'sawtooth', 0.05)
    setTimeout(() => playTone(200, 0.06, 'sawtooth', 0.04), 50)
  },
  click: () => playTone(600, 0.04, 'sine', 0.06),
}

export const useAudioStore = defineStore('audio', () => {
  const muted = ref(localStorage.getItem('audio_muted') === 'true')

  function play(name) {
    if (muted.value) return
    const fn = SYNTHS[name]
    if (fn) fn()
  }

  function toggleMute() {
    muted.value = !muted.value
    localStorage.setItem('audio_muted', muted.value.toString())
  }

  return { muted, play, toggleMute }
})
