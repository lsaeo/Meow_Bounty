# 猫咪成长系统 · Cat Evolution System

## 技术栈
- 后端：Python PIL / tkinter（修改 pet_engine.py）
- 精灵图：已有 `sprites/`（普通） + `wizard_sprites/`（魔法），需新增 2 套中间形态
- 触发：监听从 Electron 读写 `hero.json`，Python 检测 level 变化

## 项目结构
```
pet/
├── sprites/
│   ├── baby/          # Lv 1-4 小奶猫（缩小版 + 奶瓶装饰）
│   ├── normal/        # Lv 5-9 见习猫（当前默认，加领巾）
│   ├── wizard/        # Lv 10-19 魔法猫（巫师帽 + 斗篷）
│   └── legendary/     # Lv 20+ 传说猫（金色斗篷 + 光环粒子）
└── pet_engine.py      # 新增进化检测 + 切换 sprites 逻辑
```

## 全局视觉与氛围

### Lv 1-4 小奶猫
- 当前猫咪缩小至 70%，头顶加一个摇摇晃晃的问号 `?`
- 走路速度减半，偶尔摔倒（播放摔倒帧）
- 完成任务的庆祝动画更夸张（原地转圈）

### Lv 5-9 见习猫
- 当前默认猫咪 + 红色领巾
- 闲置时偶尔拿小本子假装写字

### Lv 10-19 魔法猫
- 已有 `wizard_sprites/` — 紫色巫��帽 + 暗紫斗篷 + 金星
- 闲置时漂浮魔法粒子（星光环绕）

### Lv 20+ 传说猫
- 金色斗篷 + 光环粒子 + 偶尔展翅跳起
- 完成史诗任务时绽放彩虹光芒

## 核心功能与交互细节

### Python 端：hero.json 轮询
在 `main.py` 的 `daily_reset_check` 线程中增加：
```python
def check_evolution(pet, adventurer):
    new_level = adventurer.level
    if new_level != pet._last_level:
        pet._last_level = new_level
        pet.evolve(new_level)

# pet_engine.py
def evolve(self, level):
    if level < 5:   d = 'baby'
    elif level < 10: d = 'normal'
    elif level < 20: d = 'wizard'
    else:            d = 'legendary'
    self.sprites = load_sprites_from(d)
    self.spawn_bubble(f'进化！Lv.{level} {self.title}')
    # 播放进化动画：短暂白光闪过后切换 sprite
```

### 精灵图目录切换
`load_sprites_from(dir_name)` 动态加载指定目录的 PNG 序列，替换当前 `self.sprites` 对象。动画帧编号命名保持一致（`idle1.png` ~ `walkingright4.png`）。

## 状态管理 (Pinia)
- 不用 Pinia，Python 端直接读 `hero.json`
- `hero.level` 字段已有

## 主进程
- 无需 Electron 改动

## 代码要求
- 进化动画用 Canvas 白色遮罩渐变实现（`after` 循环调节遮罩透明度）
- 如果某阶段 sprite 目录不存在，自动回退到 `normal/`
- 初始精灵图目录在 `pet_engine.__init__` 中根据 `adventurer.level` 决定
