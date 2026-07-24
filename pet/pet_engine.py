import tkinter as tk
import tkinter.font as tkfont
import random
import time
import json
import os
import sys
from win32api import GetMonitorInfo, MonitorFromPoint

from .animations import SpriteLoader, Animator, AnimationState

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get('Work')
SCREEN_WIDTH = work_area[2]
SCREEN_HEIGHT = work_area[3]

IDLE_DELAY = 400
WALK_DELAY = 100
PET_WIDTH = 72
PET_HEIGHT = 64

BUBBLE_BG = '#2c1810'
BUBBLE_BORDER = '#8b6914'
BUBBLE_TEXT = '#f0c040'
BUBBLE_TAIL_H = 12
BUBBLE_PAD_X = 14
BUBBLE_PAD_Y = 10
BUBBLE_RADIUS = 10
BUBBLE_MAX_W = 260


class SpeechBubble:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.config(bg='black')
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.withdraw()

        self.canvas = tk.Canvas(self.window, bg='black', highlightthickness=0, bd=0)
        self.canvas.pack()

        self.hide_timer = None
        self._lines = []

    def show(self, x, y, text, duration=2500, border_color=None):
        if self.hide_timer:
            self.window.after_cancel(self.hide_timer)

        self._lines = text.split('\n')
        self.canvas.delete('all')

        border = border_color or BUBBLE_BORDER

        fm = tkfont.Font(family='Microsoft YaHei', size=11)
        max_line_w = 0
        line_heights = []
        for line in self._lines:
            w = fm.measure(line)
            max_line_w = max(max_line_w, min(w, BUBBLE_MAX_W - BUBBLE_PAD_X * 2))
            line_heights.append(w)

        line_h = fm.metrics('linespace') + 2
        text_h = line_h * len(self._lines)

        bw = max(60, int(max_line_w) + BUBBLE_PAD_X * 2 + 4)
        bh = text_h + BUBBLE_PAD_Y * 2 + BUBBLE_TAIL_H

        # rounded rect body
        self._draw_rounded_rect(0, 0, bw, bh - BUBBLE_TAIL_H,
                                BUBBLE_RADIUS, fill=BUBBLE_BG, outline=border, width=2)

        # tail triangle pointing down toward pet
        tail_cx = bw // 2
        self.canvas.create_polygon(
            tail_cx - 7, bh - BUBBLE_TAIL_H - 1,
            tail_cx + 7, bh - BUBBLE_TAIL_H - 1,
            tail_cx, bh - 1,
            fill=BUBBLE_BG, outline=border, width=2
        )

        # draw text lines
        for i, line in enumerate(self._lines):
            self.canvas.create_text(
                bw // 2, BUBBLE_PAD_Y + line_h * i + line_h // 2,
                text=line, font=('Microsoft YaHei', 11),
                fill=BUBBLE_TEXT, anchor='center', width=max_line_w
            )

        bx = max(0, min(x + PET_WIDTH // 2 - bw // 2, SCREEN_WIDTH - bw))
        by = max(8, y - bh - 16)
        self.window.geometry(f'{bw}x{bh}+{bx}+{by}')
        self.window.deiconify()
        self.window.lift()
        self.hide_timer = self.window.after(duration, self.hide)

    def _draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        pts = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]
        self.canvas.create_polygon(pts, smooth=True, **kwargs)

    def hide(self):
        self.window.withdraw()
        self.hide_timer = None


class QuestPet:
    DIALOGUE_BORDERS = {
        'on_complete': '#5ad8a0',
        'on_level_up': '#f0d060',
        'on_idle': '#908878',
        'on_daily_refresh': '#f0d060',
        'on_all_clear': '#f0d060',
        'on_click': '#c9a84c',
    }

    def __init__(self, on_click_callback=None):
        self.window = tk.Tk()
        self.window.title('QuestPet')

        self.on_click_callback = on_click_callback
        self.on_quest_board = None
        self.clock_widget = None
        self.sprites = SpriteLoader()
        self.anim = Animator(self.sprites)

        self.x = int(SCREEN_WIDTH * 0.8)
        self.y = SCREEN_HEIGHT - PET_HEIGHT

        self.window.config(highlightbackground='black')
        self.label = tk.Label(self.window, bd=0, bg='black')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'black')

        self.label.pack()
        self.label.bind('<Button-1>', self._on_press)
        self.label.bind('<ButtonRelease-1>', self._on_release)
        self.label.bind('<Button-3>', self._on_right_click)
        self.label.bind('<B1-Motion>', self._on_drag)

        self._drag_start_x = 0
        self._drag_start_y = 0
        self._dragged = False

        self.bubble = SpeechBubble(self.window)

        self._event_number = random.randint(1, 18)
        self._tick_count = 0
        self._auto_state = AnimationState.IDLE
        self._direction = 1

        self._last_interaction = time.time()
        self._last_line = {}
        self._idle_said_at = 0
        self._dialogue = self._load_dialogue()

    def _load_dialogue(self):
        base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, 'dialogue.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                'on_click': ['喵？'],
                'on_idle': ['好无聊...来看看悬赏板吧？'],
                'on_daily_refresh': ['新的一天！悬赏板已刷新~'],
                'on_complete': ['干得好喵！'],
                'on_level_up': ['升级了喵！'],
                'on_all_clear': ['全部完成！'],
            }

    def say(self, category, **kwargs):
        lines = self._dialogue.get(category, ['喵？'])
        # Avoid repeating the last line for this category
        choices = [l for l in lines if l != self._last_line.get(category)]
        if not choices:
            choices = lines
        text = random.choice(choices)
        self._last_line[category] = text
        if '{task_name}' in text and 'task_name' not in kwargs:
            kwargs.setdefault('task_name', '悬赏')
        kwargs.setdefault('level', '?')
        kwargs.setdefault('title', '勇者')
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
        border = self.DIALOGUE_BORDERS.get(category)
        self.spawn_bubble(text, duration=3000, border_color=border)
        self._last_interaction = time.time()

    def spawn_bubble(self, text, duration=2500, border_color=None):
        self.bubble.show(self.x, self.y, text, duration, border_color)

    def notify_complete(self, task_name='悬赏'):
        self.say('on_complete', task_name=task_name)

    def notify_all_clear(self):
        self.say('on_all_clear')

    def notify_level_up(self, level=1, title='勇者'):
        self.say('on_level_up', level=level, title=title)

    def _on_press(self, event):
        self._last_interaction = time.time()
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root
        self._dragged = False

    def _on_release(self, event):
        if not self._dragged:
            self.say('on_click')

    def _on_drag(self, event):
        dx = event.x_root - self._drag_start_x
        dy = event.y_root - self._drag_start_y
        if abs(dx) < 2 and abs(dy) < 2:
            return
        self._dragged = True
        self.x += dx
        self.y += dy
        self._update_position()
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def _on_right_click(self, event):
        self._last_interaction = time.time()
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label=' 悬赏令', command=self._open_quest_board)
        menu.add_command(label=' 时钟', command=self._open_clock)
        menu.add_separator()
        menu.add_command(label='退出', command=self.window.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    def _open_quest_board(self):
        if self.on_quest_board:
            self.on_quest_board()

    def _open_clock(self):
        if self.clock_widget:
            self.clock_widget.show()

    def show_reward(self, exp=0, gold=0, text=None):
        if text:
            self.spawn_bubble(text, 2500)

    def show_penalty(self, hp_loss=0):
        t = f'昨夜悬赏未完成...\nHP -{hp_loss}'
        self.spawn_bubble(t, 3000)

    def celebrate(self):
        self.anim.play(self.sprites.idle, loops=3, on_end=self._restore_auto)
        self._tick_count = 0
        for _ in range(3):
            self._jump()
            self.window.update()
            time.sleep(0.08)

    def _jump(self):
        orig_y = self.y
        for offset in [-8, -16, -8, 0]:
            self.y = orig_y + offset
            self._update_position()
            self.window.update()
            time.sleep(0.05)
        self.y = orig_y

    def _restore_auto(self):
        self._tick_count = 0
        self._auto_state = AnimationState.IDLE
        self.anim.set_state(AnimationState.IDLE)
        self.anim.current_animation = self.sprites.idle

    def run(self):
        self._update_position()
        self.window.after(1, self._auto_tick)
        self.window.mainloop()

    def _auto_tick(self):
        self._tick_count += 1

        if self._tick_count > 50:
            roll = random.randint(1, 18)
            self._tick_count = 0
            if 1 <= roll <= 11:
                self._auto_state = AnimationState.IDLE
            elif roll == 12:
                self._auto_state = AnimationState.IDLE
            elif 13 <= roll <= 15:
                self._auto_state = AnimationState.WALK_LEFT
                self._direction = -1
            elif 16 <= roll <= 18:
                self._auto_state = AnimationState.WALK_RIGHT
                self._direction = 1

        if self._auto_state == AnimationState.IDLE:
            self.anim.current_animation = self.sprites.idle
            delay = IDLE_DELAY
        elif self._auto_state == AnimationState.WALK_LEFT and self.x > 0:
            self.anim.current_animation = self.sprites.walk_left
            self.x -= 3
            delay = WALK_DELAY
        elif self._auto_state == AnimationState.WALK_RIGHT and self.x < (SCREEN_WIDTH - PET_WIDTH):
            self.anim.current_animation = self.sprites.walk_right
            self.x += 3
            delay = WALK_DELAY
        else:
            self.anim.current_animation = self.sprites.idle
            delay = IDLE_DELAY

        self.anim.advance()
        self._update_position()
        self.label.configure(image=self.anim.current_frame())

        # Idle dialogue: every ~25s check if idle > 30 min
        if self._tick_count % 10 == 0:
            now = time.time()
            if now - self._last_interaction > 1800 and now - self._idle_said_at > 1800:
                self.say('on_idle')
                self._idle_said_at = now

        self.window.after(delay, self._auto_tick)

    def _update_position(self):
        self.window.geometry(f'{PET_WIDTH}x{PET_HEIGHT}+{self.x}+{self.y}')
