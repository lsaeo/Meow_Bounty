import sys
import os
import threading
import time
import subprocess
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pet.pet_engine import QuestPet
from quest.adventurer import Adventurer
from quest.rpg_engine import RPGEngine
from quest.task_manager import TaskManager, quest_today
from quest.paths import init_user_data
from pet.clock_widget import ClockWidget

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTBOARD_DIR = os.path.join(BASE_DIR, 'questboard')
_questboard_proc = None


def launch_questboard():
    """Launch the Electron quest panel, killing any previous instance first."""
    global _questboard_proc
    try:
        if _questboard_proc and _questboard_proc.poll() is None:
            _questboard_proc.terminate()
            try: _questboard_proc.wait(timeout=3)
            except: pass
        electron_exe = os.path.join(QUESTBOARD_DIR, 'node_modules', 'electron', 'dist', 'electron.exe')
        _questboard_proc = subprocess.Popen(
            [electron_exe, '.'], cwd=QUESTBOARD_DIR,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
    except Exception as e:
        print(f'Failed to launch quest board: {e}')


def daily_reset_check(adventurer, rpg_engine, task_manager, pet):
    while True:
        time.sleep(60)
        now = datetime.now()
        qt = quest_today()
        if now.hour >= 8 and adventurer.last_login != qt:
            yesterday_incomplete = task_manager.get_yesterday_incomplete()
            if yesterday_incomplete:
                total_hp, count = rpg_engine.daily_settlement(yesterday_incomplete)
                pet.show_penalty(total_hp)
            else:
                adventurer.streak += 1

            adventurer.last_login = qt
            adventurer.save()
            task_manager.advance_tomorrow_to_today()
            pet.say('on_daily_refresh')


def main():
    init_user_data()
    adventurer = Adventurer.load()
    rpg_engine = RPGEngine(adventurer)
    task_manager = TaskManager()

    pet = QuestPet()

    clock_widget = ClockWidget()
    pet.clock_widget = clock_widget
    pet.on_quest_board = launch_questboard

    monitor_thread = threading.Thread(
        target=daily_reset_check,
        args=(adventurer, rpg_engine, task_manager, pet),
        daemon=True
    )
    monitor_thread.start()

    pet.spawn_bubble(
        f'欢迎回来，{adventurer.title}！\n'
        f'右键打开悬赏版，开始今天的冒险吧！',
        5000
    )

    pet.run()


if __name__ == '__main__':
    main()
