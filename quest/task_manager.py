import json
import os
import sys
from datetime import date, datetime, timedelta
import uuid

from .paths import user_data_dir

DATA_DIR = user_data_dir()

DIFFICULTY_ICONS = {'普通': '\u2694', '困难': '\U0001f6e1', '史诗': '\U0001f451'}


def quest_today():
    """Return quest date string based on 8:00 AM Beijing time cutoff."""
    now = datetime.now()
    if now.hour < 8:
        return str((now - timedelta(days=1)).date())
    return str(now.date())


def quest_tomorrow():
    """Return tomorrow's quest date string."""
    return str(datetime.strptime(quest_today(), '%Y-%m-%d').date() + timedelta(days=1))


def quest_yesterday():
    """Return yesterday's quest date string."""
    return str(datetime.strptime(quest_today(), '%Y-%m-%d').date() - timedelta(days=1))


class TaskManager:
    def __init__(self):
        self._tasks = []
        self._load()

    def _get_path(self):
        return os.path.join(DATA_DIR, 'tasks.json')

    def _load(self):
        path = self._get_path()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self._tasks = json.load(f)
        else:
            self._tasks = []

    def _save(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(self._get_path(), 'w', encoding='utf-8') as f:
            json.dump(self._tasks, f, ensure_ascii=False, indent=2)

    def get_today_tasks(self):
        return [t for t in self._tasks if t.get('date') == quest_today()]

    def get_tomorrow_tasks(self):
        return [t for t in self._tasks if t.get('date') == quest_tomorrow()]

    def get_all_tasks(self):
        return self._tasks

    def add_task(self, name, difficulty='普通', category='日常', for_tomorrow=False,
                 original_name=None):
        target_date = quest_tomorrow() if for_tomorrow else quest_today()

        task = {
            'id': str(uuid.uuid4())[:8],
            'name': name,
            'difficulty': difficulty,
            'category': category,
            'date': target_date,
            'completed': False,
            'created_at': datetime.now().isoformat(),
        }
        if original_name and original_name != name:
            task['original_name'] = original_name
        self._tasks.append(task)
        self._save()
        return task

    def complete_task(self, task_id):
        today = quest_today()
        for t in self._tasks:
            if t['id'] == task_id:
                if t.get('date') != today:
                    return None
                t['completed'] = True
                self._save()
                return t
        return None

    def uncomplete_task(self, task_id):
        for t in self._tasks:
            if t['id'] == task_id:
                t['completed'] = False
                self._save()
                return t
        return None

    def delete_task(self, task_id):
        self._tasks = [t for t in self._tasks if t['id'] != task_id]
        self._save()

    def get_pending_incomplete(self):
        return [t for t in self._tasks if t.get('date') == quest_today() and not t['completed']]

    def advance_tomorrow_to_today(self):
        today = quest_today()
        changed = 0
        for t in self._tasks:
            if t.get('date') < today:
                t['date'] = str(datetime.strptime(today, '%Y-%m-%d').date() + timedelta(days=1))
                t['completed'] = False
                changed += 1
        if changed:
            self._save()
        return changed

    def get_yesterday_incomplete(self):
        yesterday = quest_yesterday()
        return [t for t in self._tasks if t.get('date') == yesterday and not t['completed']]

    def today_completion_rate(self):
        today_tasks = self.get_today_tasks()
        if not today_tasks:
            return None
        completed = sum(1 for t in today_tasks if t.get('completed', False))
        return completed, len(today_tasks)
