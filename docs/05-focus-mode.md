# 专注模式 · Focus Mode

## 技术栈
- 前端：Vue 3 + GSAP 计时器动画
- 计时：`setInterval` 驱动的倒计时
- 奖励：完成计时 → 触发 `questStore` 金币奖励
- 背景：CSS 全屏遮罩 + 径向渐变模拟光晕

## 项目结构
```
questboard/src/
├── stores/
│   └── focus.js           # 专注状态管理
└── components/
    └── FocusMode.vue       # 专注面板
```

## 全局视觉与氛围
- 全屏暗蓝遮罩（`rgba(5,5,20,.95)`），中央一个发光的沙漏
- 沙漏用 Canvas 或 CSS 绘制：上瓶 → 下瓶漏沙动画
- 中央大号倒计时数字（`HH:MM:SS`），字体 48px，金色发光
- 下方预设时间按钮：25 分 / 45 分 / 60 分（番茄钟风格）
- 底部 "开始专注" 按钮 → 变 "放弃"（放弃无奖励）
- 计时结束 → 沙漏翻转 → 弹出 "专注完成！+50 金币"

## 核心功能与交互细节

### FocusStore
```js
export const useFocusStore = defineStore('focus', () => {
  const active = ref(false)
  const remaining = ref(0)    // 秒
  const total = ref(0)
  const intervalId = ref(null)
  const reward = computed(() => Math.floor(total.value / 60) * 2) // 每分钟 2 金币

  function start(minutes) {
    total.value = minutes * 60
    remaining.value = total.value
    active.value = true
    intervalId.value = setInterval(tick, 1000)
  }

  function tick() {
    if (remaining.value <= 0) {
      clearInterval(intervalId.value)
      active.value = false
      // 触发奖励 (callback to questStore)
    }
    remaining.value--
  }

  function abort() {
    clearInterval(intervalId.value)
    active.value = false
    remaining.value = 0
  }

  return { active, remaining, total, reward, start, abort }
})
```

### 奖励结算
计时结束后回调 `questStore.hero.gold += focusStore.reward`，写入 `hero.json`。

## 状态管理 (Pinia)
- `focusStore` 独立 store
- 不持久化（每次打开都是全新计时）

## 主进程
- 可选：通知 `Notification API` 在计时结束时弹出系统通知

## 代码要求
- 计时期间面板禁止关闭（`hide()` 不响应或弹出确认）
- 倒计时精确到秒
- 支持暂停/继续（非 MVP，可后续添加）
