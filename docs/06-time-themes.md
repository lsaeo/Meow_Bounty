# 时段主题 · Time-based Themes

## 技术栈
- 前端：CSS 变量动态切换
- 触发：`setInterval` 每 60 秒检查当前时段
- 数据：无需持久化，纯客户端计算

## 项目结构
```
questboard/src/
├── stores/
│   └── theme.js           # 主题状态管理
├── App.vue                # 根组件应用 CSS 变量
└── assets/
    └── themes/
        ├── dawn.css        # 6:00-12:00 晨曦
        ├── day.css         # 12:00-18:00 白昼
        └── night.css       # 18:00-6:00 暗夜
```

## 全局视觉与氛围

| 时段 | 时间 | 背景色 | 粒子色 | 边框色 | 氛围 |
|------|------|--------|--------|--------|------|
| 🌅 晨曦 | 6:00-12:00 | 渐变 `#2a1a3a → #4a3050 → #c8a860` | 金色 + 淡粉 | 铜金 | 温暖曙光 |
| ☀️ 白昼 | 12:00-18:00 | 渐变 `#1a3a2a → #205040 → #8ac850` | 绿色 + 金色 | 翠金 | 生机盎然 |
| 🌙 暗夜 | 18:00-6:00 | 渐变 `#06061a → #101030 → #0a0a1c`（当前） | 蓝紫 + 金色 | 紫金 | 神秘夜晚 |

## 核心功能与交互细节

### ThemeStore
```js
export const useThemeStore = defineStore('theme', () => {
  const current = ref('night')

  function detect() {
    const h = new Date().getHours()
    if (h >= 6 && h < 12) current.value = 'dawn'
    else if (h >= 12 && h < 18) current.value = 'day'
    else current.value = 'night'
  }

  // CSS 变量映射
  const vars = computed(() => ({
    '--bg-deep':   current.value === 'dawn' ? '#1a1030' : current.value === 'day' ? '#0a1a14' : '#06061a',
    '--accent':    current.value === 'dawn' ? '#e8a060' : current.value === 'day' ? '#60c880' : '#6088f0',
    '--gold-dim':  current.value === 'dawn' ? '#c88050' : current.value === 'day' ? '#70a050' : '#887030',
    '--gold':      current.value === 'dawn' ? '#e8b870' : current.value === 'day' ? '#80d870' : '#c9a84c',
    '--gold-bright': current.value === 'dawn' ? '#f0d080' : current.value === 'day' ? '#a0f080' : '#f0d060',
  }))

  onMounted(() => { detect(); setInterval(detect, 60000) })

  return { current, vars, detect }
})
```

### 应用
`App.vue` 中 `:style="themeStore.vars"` 绑定到根元素，所有 `var(--xxx)` 自动切换。

## 状态管理 (Pinia)
- `themeStore` 独立 store
- 不持久化

## 主进程
- 无需改动

## 代码要求
- 切换时无闪烁，通过 CSS transition 平滑过渡（`transition: all 3s ease`）
- 时段边界（如 11:59 → 12:00）切换无跳变
- 当前版本只有一个 theme（night），新增的 dawn/day 为可选 CSS
