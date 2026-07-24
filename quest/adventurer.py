import json
import os
from datetime import date, datetime

from .task_manager import quest_today
from .paths import user_data_dir

DATA_DIR = user_data_dir()


class Adventurer:
    TITLES = {
        1: '初心勇者',
        5: '见习骑士',
        10: '王国骑士',
        15: '圣殿骑士',
        20: '龙骑士',
        25: '皇家守护者',
        30: '传说英雄',
        40: '半神勇者',
        50: '创世勇者',
    }

    def __init__(self, name='勇者'):
        self.name = name
        self.level = 1
        self.exp = 0
        self.hp = 100
        self.max_hp = 100
        self.gold = 0
        self.streak = 0
        self.last_login = quest_today()

    @property
    def exp_to_next(self):
        return self.level * 100

    @property
    def title(self):
        current = '初心勇者'
        for lv, t in sorted(self.TITLES.items()):
            if self.level >= lv:
                current = t
        return current

    def add_exp(self, amount):
        self.exp += amount
        leveled_up = False
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.max_hp += 10
            self.hp = min(self.hp + 20, self.max_hp)
            leveled_up = True
        return leveled_up

    def add_gold(self, amount):
        self.gold += amount

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return self.hp <= 0

    def check_daily(self):
        qt = quest_today()
        if self.last_login != qt:
            self.last_login = qt
            return True
        return False

    def to_dict(self):
        return {
            'name': self.name,
            'level': self.level,
            'exp': self.exp,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'gold': self.gold,
            'streak': self.streak,
            'last_login': self.last_login,
        }

    @classmethod
    def from_dict(cls, data):
        a = cls(data.get('name', '勇者'))
        a.level = data.get('level', 1)
        a.exp = data.get('exp', 0)
        a.hp = data.get('hp', 100)
        a.max_hp = data.get('max_hp', 100)
        a.gold = data.get('gold', 0)
        a.streak = data.get('streak', 0)
        a.last_login = data.get('last_login', '')
        return a

    @classmethod
    def load(cls):
        path = os.path.join(DATA_DIR, 'hero.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return cls.from_dict(json.load(f))
        return cls()

    def save(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        path = os.path.join(DATA_DIR, 'hero.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
