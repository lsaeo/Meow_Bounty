# Boss 副本 · Boss Dungeon

## 技术栈
- 前端：Vue 3 组件 + GSAP 战斗动画 + Pinia
- Boss 数据：JSON 配置文件（预设 Boss 池）
- 触发：时间条件 + 任务完成条件

## 项目结构
```
questboard/src/
├── stores/
│   └── boss.js            # Boss 状态管理
├── components/
│   └── BossBattle.vue     # Boss 战斗面板
└── data/
    └── bosses.json        # Boss 数据池
```

## 全局视觉与氛围

### Boss 面板
- 全屏暗红遮罩，中央 Boss 卡片
- Boss 图片：用 CSS/SVG 绘制巨型怪物剪影（初始可用简单几何 + 文字替代）
- HP 条：宽红色血条，受到史诗任务完成伤害时减少
- Boss 名称 + 描述文字
- 下方 "悬赏槽位"：3 个空槽，每个对应一个史诗任务

### Boss 数据格式
```json
{
  "id": "dragon_1",
  "name": "暗影巨龙",
  "desc": "沉睡在火山深处的远古恶龙，只有史诗级悬赏才能伤到它的鳞片。",
  "hp": 3,
  "maxHp": 3,
  "weakness": "史诗",
  "reward_gold": 200,
  "reward_title": "屠龙者",
  "icon": "🐉"
}
```

### Boss 池
| Boss | HP | 弱点 | 奖励 |
|------|-----|------|------|
| 🐉 暗影巨龙 | 3 | 史诗 | 200G + "屠龙者" |
| 💀 不死将军 | 3 | 史诗 | 150G + "亡灵克星" |
| 👁 深渊之眼 | 3 | 史诗 | 250G + "窥秘者" |
| 🗡 暗黑骑士 | 4 | 史诗 | 300G + "光明使者" |

## 核心功能与交互细节

### 刷新机制
每周六 8:00 自动刷新一只新 Boss（配合 quest_today 逻辑）。

```js
function checkBossRefresh() {
  const now = new Date()
  if (now.getDay() !== 6) return  // 只在周六
  if (lastBossDate === questToday()) return  // 已刷新
  const boss = pickRandomBoss()
  currentBoss.value = { ...boss, hp: boss.maxHp }
  lastBossDate = questToday()
}
```

### 战斗流程
```
1. 用户在普通面板完成「史诗」任务
   → boss.takeDamage(1)
   → GSAP: Boss HP 条缩减 + Boss 抖动 + 屏幕短暂红光

2. 当 boss.hp === 0
   → Boss 爆炸动画（碎裂扩散）
   → 弹出 "击败 {boss.name}！"
   → 奖励：金币 + 称号 + 解锁成就
   → currentBoss = null

3. 周六 8:00 前未击败
   → Boss 逃走（无惩罚）
   → "Boss 已逃离，下周再来..."
```

### BossStore
```js
export const useBossStore = defineStore('boss', () => {
  const currentBoss = ref(null)
  const defeatedBosses = ref([])

  function takeDamage() {
    if (!currentBoss.value) return
    currentBoss.value.hp--
    if (currentBoss.value.hp <= 0) {
      defeatedBosses.value.push(currentBoss.value.id)
      // 奖励结算
      currentBoss.value = null
    }
  }

  return { currentBoss, defeatedBosses, takeDamage, checkBossRefresh }
})
```

### 集成点
- `questStore.completeTask()` 中检查 `task.difficulty === '史诗'` → `bossStore.takeDamage()`
- 面板顶部如果有活跃 Boss → 显示 Boss 血条和名称

## 状态管理 (Pinia)
- `bossStore` 独立 store
- `defeatedBosses` 持久化到 `localStorage`
- `currentBoss` 在 session 内有效

## 主进程
- 无需改动

## 代码要求
- Boss 战斗动画用 GSAP（血条缩减 + 抖动）
- Boss 死亡动画用 GSAP scale + opacity 碎裂
- 至少预设 4 个 Boss，随机选择
