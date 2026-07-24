# 音效系统 · Sound Effects System

## 技术栈
- 前端：`HTML5 Audio API`（Electron renderer 中直接 `new Audio()`）
- 音源：免费音效站 [freesound.org](https://freesound.org) / [mixkit.co](https://mixkit.co) 下载 `.mp3`
- 存储：`questboard/src/assets/sounds/` 目录
- 播放控制：Pinia store 中 `audioStore` 管理全局音量/静音

## 项目结构
```
questboard/src/
├── stores/
│   └── audio.js          # 音效状态管理
├── assets/
│   └── sounds/
│       ├── complete.mp3   # 完成任务 — 剑击/金币
│       ├── levelup.mp3    # 升级 — 号角/圣光
│       ├── post.mp3       # 张贴悬赏 — 羊皮纸/印章
│       ├── allclear.mp3   # 全清 — 钟声/欢呼
│       └── delete.mp3     # 删除悬赏 — 撕纸
```

## 全局视觉与氛围
- 不涉及视觉变更，纯听觉增强
- 面板顶部右侧增加一个小喇叭图标 🔊/🔇 切换静音

## 核心功能与交互细节

### AudioStore (`stores/audio.js`)
```js
export const useAudioStore = defineStore('audio', () => {
  const muted = ref(false)
  const volume = ref(0.6)

  const cache = {}  // { 'complete': HTMLAudioElement }

  function preload(name) {
    if (cache[name]) return
    const a = new Audio(`./assets/sounds/${name}.mp3`)
    a.volume = volume.value
    cache[name] = a
  }

  function play(name) {
    if (muted.value) return
    if (!cache[name]) preload(name)
    const a = cache[name]
    a.currentTime = 0
    a.play().catch(() => {})
  }

  function toggleMute() { muted.value = !muted.value }

  return { muted, volume, preload, play, toggleMute }
})
```

### 触发时机
| 事件 | 音效 | 时机 |
|------|------|------|
| completeTask() | `complete.mp3` | 勾选完成时 |
| 升级检测在 completeTask 中 | `levelup.mp3` | 经验溢出升级时 |
| addTask() | `post.mp3` | 张贴悬赏时 |
| apply_all_clear_bonus | `allclear.mp3` | 今日全清时 |
| deleteTask() | `delete.mp3` | 删除悬赏时 |

### 预加载
在 `App.vue` 的 `onMounted` 中调用 `audioStore.preload()` 预加载全部音效文件。

## 状态管理 (Pinia)
- `audioStore` 独立 store
- `muted` 持久化到 `localStorage`

## 主进程
- 无需 Electron 主进程改动
- HTML5 Audio 在 renderer 进程运行

## 代码要求
- `new Audio()` 在 Electron 中直接可用，无需 `nodeIntegration`
- 所有音效文件 < 50KB，不阻塞加载
- 音效播放使用 `play().catch(() => {})` 防止 autoplay policy 报错
- 提供降级方案：音效文件缺失时不报错，静默跳过
