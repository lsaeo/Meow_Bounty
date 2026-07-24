# 成就徽章 · Achievement Badges

## 技术栈
- 前端：Vue 3 组件 + Pinia
- 动画：GSAP 弹入/淡出
- 数据：`localStorage` 持久化已解锁徽章列表
- 图标：内联 SVG（盾牌/星星/皇冠等简单几何图形）

## 项目结构
```
questboard/src/
├── stores/
│   └── achievements.js   # 成就状态管理
├── components/
│   ├── BadgePopup.vue     # 解锁弹窗（居中弹出）
│   └── BadgeList.vue      # 成就展示面板
└── assets/
    └── badges/             # 徽章 SVG 图标（可选，也可内联）
```

## 全局视觉与氛围

### BadgePopup
- 居中玻璃拟态卡片，金色边框
- 顶部大号徽章图标（圆形，金色渐变底 + 白色符号）
- 成就名称 + 描述文字
- 下方金色 "获得成就！" 按钮
- 自动 4 秒后消失，或点击关闭
- GSAP 入场：`scale(0) → scale(1.2) → scale(1)` 弹性动画

### BadgeList
- 荣誉殿堂的子页，或独立面板
- 网格排列已解锁徽章，未解锁显示灰色锁定态
- 进度条显示接近解锁的成就

## 核心功能与交互细节

### 成就列表

| 成就 ID | 名称 | 描述 | 触发条件 |
|---------|------|------|----------|
| `first_quest` | 初出茅庐 | 张贴并完成第一个悬赏 | `completedTasks >= 1` |
| `streak_7` | 全勤勇士 | 连续 7 天完成所有悬赏 | `hero.streak >= 7` |
| `hundred` | 百战英豪 | 累计完成 100 个悬赏 | `completedTasks >= 100` |
| `gold_1000` | 赏金猎人 | 累计金币达到 1000 | `hero.gold >= 1000` |
| `epic_5` | 史诗杀手 | 完成 5 个史诗悬赏 | `completedEpicCount >= 5` |
| `speedrun` | 闪电勇者 | 发布后 10 分钟内完成 | `completedAt - createdAt <= 10min` |
| `perfect_week` | 完美一周 | 连续 7 天无未完成惩罚 | `streak >= 7 且无 hp 损失` |

### 触发流程
```
store.completeTask()
  → 更新任务/英雄数据
  → achievements.checkAll()
      → 遍历所有成就条件
      → 发现新解锁 → achievements.unlock(id) → 弹出 BadgePopup
      → 写入 localStorage
```

### AchievementsStore
```js
const ACHIEVEMENTS = [
  { id: 'first_quest', name: '初出茅庐', desc: '完成第一个悬赏', icon: 'sword',
    check: (store) => store.completedTasks.length >= 1 },
  { id: 'streak_7', name: '全勤勇士', desc: '连续7天完成所有悬赏', icon: 'star',
    check: (store) => store.hero.streak >= 7 },
  // ...
]
```

## 状态管理 (Pinia)
- `achievementsStore` 独立 store
- `unlocked: Ref<string[]>` 已解锁 ID 列表
- `checkAll(questStore)` — 遍历所有成就检测
- `unlock(id)` — 推入列表 + 弹窗 + 持久化
- 在 `completeTask` / `addTask` / 每日重置后调用 `checkAll`

## 主进程
- 无需 Electron 主进程改动

## 代码要求
- 弹窗用 `fixed` 定位，z-index 高于所有面板
- 弹窗同时只显示一个，积压的成就排队弹出
- 已解锁徽章数据存 `localStorage`，重启不丢失
- 提供至少 5 个可解锁成就作为 MVP
