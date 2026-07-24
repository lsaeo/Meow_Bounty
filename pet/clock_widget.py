"""Medieval-themed desktop clock widget using Pillow + tkinter."""

import tkinter as tk
import time
import math

from PIL import Image, ImageDraw, ImageTk, ImageFilter

CLOCK_SIZE = 180
CENTER = CLOCK_SIZE // 2
R = CENTER - 12

# Colors
WOOD_BG = (62, 34, 22)
GOLD = (200, 168, 72)
GOLD_LIGHT = (230, 200, 100)
HAND_DARK = '#e8c050'
HAND_RED = '#e84040'

def _rgb(hex_str):
    return tuple(int(hex_str[i:i+2], 16) for i in (1, 3, 5))


def _draw_clock_face():
    """Generate a static clock face image."""
    img = Image.new('RGBA', (CLOCK_SIZE, CLOCK_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer ring
    draw.ellipse([4, 4, CLOCK_SIZE - 5, CLOCK_SIZE - 5],
                 fill=WOOD_BG, outline='#c8a848', width=3)
    draw.ellipse([10, 10, CLOCK_SIZE - 11, CLOCK_SIZE - 11],
                 outline='#c8a848', width=1)

    # Center circle
    draw.ellipse([CENTER - 5, CENTER - 5, CENTER + 5, CENTER + 5],
                 fill='#c8a848')

    # Roman numerals at 12, 3, 6, 9 positions
    numerals = {
        12: 'XII', 1: 'I', 2: 'II', 3: 'III',
        4: 'IV', 5: 'V', 6: 'VI',
        7: 'VII', 8: 'VIII', 9: 'IX',
        10: 'X', 11: 'XI',
    }
    r_num = R - 18
    for h, text in numerals.items():
        angle = math.radians(h * 30 - 90)
        x = CENTER + r_num * math.cos(angle)
        y = CENTER + r_num * math.sin(angle)
        draw.text((x - 7, y - 6), text, fill='#e6c864')

    # Hour markers (small dots)
    r_dot = R - 5
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        x = CENTER + r_dot * math.cos(angle)
        y = CENTER + r_dot * math.sin(angle)
        if i % 5 == 0:
            draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill='#c8a848')
        else:
            draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(160, 130, 80))

    return img


class ClockWidget:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.config(bg='black')
        self.window.withdraw()

        self.face_img = _draw_clock_face()
        self.face_tk = ImageTk.PhotoImage(self.face_img)

        self.canvas = tk.Canvas(self.window, width=CLOCK_SIZE, height=CLOCK_SIZE,
                                bg='black', highlightthickness=0, bd=0)
        self.canvas.pack()

        # Dragging
        self.canvas.bind('<Button-1>', self._start_drag)
        self.canvas.bind('<B1-Motion>', self._do_drag)

        self.canvas.create_image(0, 0, image=self.face_tk, anchor='nw')

        self._hands = {}
        self._running = False
        self._after_id = None

    def _start_drag(self, event):
        self._drag_x = event.x_root
        self._drag_y = event.y_root
        return 'break'

    def _do_drag(self, event):
        dx = event.x_root - self._drag_x
        dy = event.y_root - self._drag_y
        x = self.window.winfo_x() + dx
        y = self.window.winfo_y() + dy
        self.window.geometry(f'+{x}+{y}')
        self._drag_x = event.x_root
        self._drag_y = event.y_root
        return 'break'

    def show(self):
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = sw - CLOCK_SIZE - 20
        y = sh - CLOCK_SIZE - 80
        self.window.geometry(f'{CLOCK_SIZE}x{CLOCK_SIZE}+{x}+{y}')
        self.window.deiconify()
        self.window.lift()
        if not self._running:
            self._running = True
            self._tick()

    def hide(self):
        self._running = False
        if self._after_id:
            self.window.after_cancel(self._after_id)
            self._after_id = None
        self.window.withdraw()

    def _tick(self):
        if not self._running:
            return
        self._draw_hands()
        self._after_id = self.window.after(1000, self._tick)

    def _draw_hands(self):
        self.canvas.delete('hands')
        now = time.localtime()
        h = now.tm_hour % 12
        m = now.tm_min
        s = now.tm_sec

        # Hour hand
        ha = math.radians((h + m / 60) * 30 - 90)
        hx = CENTER + (R - 45) * math.cos(ha)
        hy = CENTER + (R - 45) * math.sin(ha)
        self.canvas.create_line(CENTER, CENTER, hx, hy,
                                fill=HAND_DARK, width=6, capstyle='round', tags='hands')

        # Minute hand
        ma = math.radians((m + s / 60) * 6 - 90)
        mx = CENTER + (R - 25) * math.cos(ma)
        my = CENTER + (R - 25) * math.sin(ma)
        self.canvas.create_line(CENTER, CENTER, mx, my,
                                fill=HAND_DARK, width=4, capstyle='round', tags='hands')

        # Second hand
        sa = math.radians(s * 6 - 90)
        sx = CENTER + (R - 20) * math.cos(sa)
        sy = CENTER + (R - 20) * math.sin(sa)
        self.canvas.create_line(CENTER + 1, CENTER + 1, sx, sy,
                                fill=HAND_RED, width=2, tags='hands')

        # Center dot
        self.canvas.create_oval(CENTER - 4, CENTER - 4, CENTER + 5, CENTER + 5,
                                fill='#c8a848', outline=HAND_DARK, tags='hands')
