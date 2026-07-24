import os
from tkinter import PhotoImage

SPRITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprites')

class AnimationState:
    IDLE = 0
    SLEEPING = 2
    WALK_LEFT = 4
    WALK_RIGHT = 5

class SpriteLoader:
    def __init__(self):
        self.idle = self._load_frames('idle', 4)
        self.idle_to_sleep = self._load_frames('sleeping', 6)
        self.sleeping = self._load_frames('zzz', 4)
        self.sleep_to_idle = self._load_frames_reversed('sleeping', 6)
        self.walk_left = self._load_frames('walkingleft', 4)
        self.walk_right = self._load_frames('walkingright', 4)
        self.angry = None
        angry_path = os.path.join(SPRITE_DIR, 'angry.png')
        if os.path.exists(angry_path):
            self.angry = PhotoImage(file=angry_path)

    def _load_frames(self, name, count):
        frames = []
        for i in range(1, count + 1):
            path = os.path.join(SPRITE_DIR, f'{name}{i}.png')
            frames.append(PhotoImage(file=path))
        return frames

    def _load_frames_reversed(self, name, count):
        frames = []
        for i in range(count, 0, -1):
            path = os.path.join(SPRITE_DIR, f'{name}{i}.png')
            frames.append(PhotoImage(file=path))
        return frames

class Animator:
    def __init__(self, sprites):
        self.sprites = sprites
        self.frame = 0
        self.state = AnimationState.IDLE
        self.current_animation = sprites.idle
        self.loop_count = 0
        self.max_loops = 0
        self._on_loop_end = None

    def set_state(self, state):
        self.state = state
        self.frame = 0

    def play(self, frames, loops=0, on_end=None):
        self.current_animation = frames
        self.frame = 0
        self.loop_count = 0
        self.max_loops = loops
        self._on_loop_end = on_end

    def advance(self):
        if self.frame < len(self.current_animation) - 1:
            self.frame += 1
        else:
            self.loop_count += 1
            self.frame = 0
            if self.max_loops > 0 and self.loop_count >= self.max_loops:
                if self._on_loop_end:
                    callback = self._on_loop_end
                    self._on_loop_end = None
                    callback()
                return True
        return False

    def current_frame(self):
        if self.frame < len(self.current_animation):
            return self.current_animation[self.frame]
        return self.current_animation[0]
