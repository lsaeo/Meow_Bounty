# 猫咪台词系统 · Cat Dialogue Lines

## 技术栈
- 后端：Python `pet_engine.py` 中 `spawn_bubble()` 扩展
- 数据：台词 JSON 配置文件
- 触发：事件钩子（完成/张贴/升级/冷落等）

## 项目结构
```
pet/
├── dialogue.json          # 台词配置（或直接在 pet_engine.py 中定义）
└── pet_engine.py          # 新增 dialogue 相关方法
```

## 全局视觉与氛围
- 使用已有气泡系统（Canvas 圆角对话框 + 金色文字）
- 不同事件类型使用不同的气泡颜色边框：
  - 完成 → 绿色 `#5ad8a0`
  - 升级 → 金色 `#f0d060`
  - 冷落 → 灰色 `#908878`
  - 错误 → 红色 `#f05068`

## 核心功能与交互细节

### 台词配置 (dialogue.json)
```json
{
  "on_complete": [
    "干得好喵！又一个悬赏搞定~",
    "委托人一定会感谢你的！",
    "这波操作很丝滑喵~",
    "金币到手！离暴富又近了一步💰",
    "喵呜！{task_name} 已被击败！"
  ],
  "on_level_up": [
    "✨ 进化之光！Lv.{level}！",
    "变强了喵！{title} 称号解锁！",
    "冒险者公会向你致敬，{title}！"
  ],
  "on_idle": [
    "好无聊...来看看悬赏板吧？",
    "今天还有任务没完成哦~",
    "摸鱼可不是好勇者的习惯喵",
    "不来张贴一个新悬赏吗？"
  ],
  "on_daily_refresh": [
    "新的一天！悬赏板已刷新~",
    "早上好喵！今天也要元气满满！",
    "昨晚的悬赏都完成了吗？"
  ],
  "on_all_clear": [
    "全部完成！你是最强的勇者！🏆",
    "完美的一天！酒馆的吟游诗人在传唱你的名字~",
    "连击 +1！继续保持喵！"
  ],
  "on_click": [
    "哎呀别戳了！",
    "有什么事？右键有菜单哦~",
    "喵？"
  ]
}
```

### 台词选择
```python
import random

DIALOGUE = load_json('dialogue.json')

def say(self, category, **kwargs):
    lines = DIALOGUE.get(category, ['喵？'])
    text = random.choice(lines).format(**kwargs)
    self.spawn_bubble(text, duration=2500)
```

### 冷落检测
在 `pet_engine.py` 中增加 `_last_interaction` 时间戳，每次鼠标点击/右键更新。`_auto_tick` 中检测：
```python
if time.time() - self._last_interaction > 1800:  # 30 分钟
    self.say('on_idle')
    self._last_interaction = time.time()  # 防止重复触发
```

### 每日刷新台词
在 `main.py` 的 `daily_reset_check` 检测到刷新时，调用 `pet.say('on_daily_refresh')`。

## 状态管理 (Pinia)
- 无，Python 端管理

## 主进程
- 无，纯 Python tkinter

## 代码要求
- 所有台词支持 `{task_name}` `{level}` `{title}` 等动态变量
- 同一事件连续触发时不重复同一句（记录上一条台词，排除重选）
- 冷落台词有冷却时间（30 分钟内不重复）
- 台词文件 JSON 格式，方便非程序员修改
