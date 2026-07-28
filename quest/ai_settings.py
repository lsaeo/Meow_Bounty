"""AI Settings manager — saves/loads API config to data/ai_settings.json."""

import json
import os

from .paths import user_data_dir

DATA = user_data_dir()

DEFAULTS = {
    'enabled': False,
    'api_key': '',
    'api_base': 'https://api.deepseek.com',
    'model': 'deepseek-chat',
    'system_prompt': (
        '你是冒险者公会的长老，负责将村民们的日常委托转化为中世纪奇幻风格的悬赏任务。'
        '规则：1) 保留原任务的核心含义，但用奇幻世界观重写；'
        '2) 控制在15字以内；3) 使用类似"讨伐""寻找""锻造""破译""护送"等动作词；'
        '4) 加入怪物、魔法、异世界元素；5) 只输出任务名，不要解释。'
        '\n\n世界观：这是一个剑与魔法的世界，有龙族、哥布林、精灵、矮人、'
        '不死族等种族。魔法分为元素、治愈、召唤、禁忌四大类。'
        '冒险者公会向勇者们发布悬赏令。'
    ),
}


def load():
    path = os.path.join(DATA, 'ai_settings.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return dict(DEFAULTS)


def save(settings):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, 'ai_settings.json'), 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
