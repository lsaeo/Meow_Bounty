"""Shared path utilities for QuestPet — dev vs frozen exe."""
import os
import sys


def base_dir():
    """Application root directory (exe location or script dir)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(sys.executable if '__file__' not in dir() else __file__))


def user_data_dir():
    """Per-user data directory — %APPDATA%/QuestPet on Windows."""
    appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
    path = os.path.join(appdata, 'QuestPet')
    os.makedirs(path, exist_ok=True)
    return path


def init_user_data():
    """Ensure default data files exist in user data dir."""
    d = user_data_dir()
    defaults = {
        'hero.json': '{"name": "勇者", "level": 1, "exp": 0, "hp": 100, "maxHp": 100, "gold": 0, "streak": 0, "last_login": ""}',
        'tasks.json': '[]',
        'ai_settings.json': '{"enabled": false, "api_key": "", "api_base": "https://api.deepseek.com", "model": "deepseek-v4-flash", "system_prompt": "你是冒险者公会的长老，负责将村民们的日常委托转化为中世纪奇幻风格的悬赏任务。规则：1) 保留原任务的核心含义，但用奇幻世界观重写；2) 控制在15字以内；3) 使用类似讨伐寻找锻造破译护送等动作词；4) 加入怪物、魔法、异世界元素；5) 只输出任务名，不要解释。"}',
    }
    for filename, content in defaults.items():
        path = os.path.join(d, filename)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
