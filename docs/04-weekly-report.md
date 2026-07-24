# 每周战报 · Weekly Battle Report

## 技术栈
- 前端：Vue 3 组件 + Pinia
- 图表：纯 CSS bar chart（不引入 Chart.js 等第三方库）
- 数据：`tasks.json` 中已完成任务的历史记录
- 触发：每周一首次打开面板时弹出

## 项目结构
```
questboard/src/
├── stores/
│   └── weekly.js          # 周报数据计算
└── components/
    └── WeeklyReport.vue    # 战报面板
```

## 全局视觉与氛围
- 一张仿羊皮纸的全屏卡片，居中弹出
- 顶部标题 "📜 第 N 周战报 · 勇者 {name}"
- 四个数据模块用金色分割线隔开：
  - "🏆 本周完成" — 大号数字
  - "💰 获得金币" — 带金币图标
  - "🔥 最长连击" — 火焰图标
  - "📜 最常委托人" — NPC 头像
- 底部对比上周的变化箭头 ↑/↓
- "关闭" → GSAP 卷起动画

## 核心功能与交互细节

### WeeklyStore
```js
export const useWeeklyStore = defineStore('weekly', () => {
  const lastShown = ref(localStorage.getItem('weekly_last_shown') || '')

  function getThisWeekTasks(tasks) {
    const now = new Date()
    const monday = new Date(now)
    monday.setDate(now.getDate() - (now.getDay() || 7) + 1)
    monday.setHours(0, 0, 0, 0)
    return tasks.filter(t => {
      const d = new Date(t.created_at)
      return d >= monday && t.completed
    })
  }

  function computeReport(tasks) {
    const weekTasks = getThisWeekTasks(tasks)
    return {
      total: weekTasks.length,
      gold: weekTasks.reduce((s, t) => s + DIFF_REWARDS[t.difficulty] || 0, 0),
      epic: weekTasks.filter(t => t.difficulty === '史诗').length,
      // last week comparison...
    }
  }

  function shouldShow() {
    const now = new Date()
    if (now.getDay() !== 1) return false  // 只在周一
    const today = now.toISOString().slice(0, 10)
    if (lastShown.value === today) return false
    lastShown.value = today
    localStorage.setItem('weekly_last_shown', today)
    return true
  }

  return { computeReport, shouldShow, lastShown }
})
```

### 触发时机
- `App.vue` 的 `onMounted` → 调用 `weeklyStore.shouldShow()`
- 返回 `true` → 弹出 `WeeklyReport` 组件

## 状态管理 (Pinia)
- `weeklyStore` 只负责日期判断和计算，不存储任务数据（复用 `questStore`）

## 主进程
- 无需 Electron 改动

## 代码要求
- 弹窗 4 秒后自动消失，或点击一键关闭
- 不弹出时不阻塞正常使用
- 历史周报可回溯查看（存 `localStorage`，key 为周次）
