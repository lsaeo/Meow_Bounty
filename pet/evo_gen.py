"""Generate significantly better evolution sprites using Pillow."""

import os
from PIL import Image, ImageDraw, ImageFilter

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprites')
BABY = os.path.join(SRC, 'baby')
LEGENDARY = os.path.join(SRC, 'legendary')
os.makedirs(BABY, exist_ok=True)
os.makedirs(LEGENDARY, exist_ok=True)

BABY_COLOR = (255, 200, 180)
LEGEND_GOLD = (255, 215, 0)
LEGEND_GLOW = (255, 240, 120)


def make_baby(src_path, dst_path):
    img = Image.open(src_path).convert('RGBA')
    w, h = img.size
    # Scale to 65%
    nw, nh = int(w * 0.65), int(h * 0.65)
    small = img.resize((nw, nh))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ox = (w - nw) // 2
    oy = h - nh
    out.paste(small, (ox, oy), small)

    draw = ImageDraw.Draw(out)
    # Cute blush cheeks
    for cx, cy in [(ox + 4, oy + nh - 10), (ox + nw - 8, oy + nh - 10)]:
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 150, 150, 180))
    # Pacifier
    px, py = ox + nw - 6, oy + nh - 16
    draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(180, 210, 255), outline=(140, 170, 220))
    draw.rectangle([px - 1, py + 2, px + 1, py + 7], fill=(160, 190, 240))
    # Tiny floating hearts
    for hx, hy in [(w//2 - 8, 4), (w//2 + 6, 8)]:
        draw.ellipse([hx - 1, hy, hx + 1, hy + 2], fill=(255, 180, 180))
        draw.ellipse([hx - 2, hy - 2, hx, hy], fill=(255, 180, 180))
        draw.ellipse([hx, hy - 2, hx + 2, hy], fill=(255, 180, 180))
    out.save(dst_path)


def make_legendary(src_path, dst_path):
    img = Image.open(src_path).convert('RGBA')
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # Glowing gold aura ring
    for i in range(3):
        r = 18 + i * 4
        draw.ellipse([w//2 - r, h//2 - r - 6, w//2 + r, h//2 + r - 6],
                     outline=(LEGEND_GOLD[0], LEGEND_GOLD[1], LEGEND_GOLD[2], 200 - i * 50), width=2)

    # Golden cape
    cx = w // 2
    for yo in range(-4, 5):
        shade = int(200 - abs(yo) * 15)
        lx = cx - 12 + abs(yo)
        rx = cx + 12 - abs(yo)
        draw.line([(lx, h - 2 + yo), (cx, h + 10 + yo), (rx, h - 2 + yo)],
                  fill=(shade, shade-40, 20), width=2)

    # Crown
    crown_y = -4
    for spike in range(3):
        sx = cx - 6 + spike * 6
        draw.polygon([(sx - 3, crown_y + 6), (sx, crown_y - 2), (sx + 3, crown_y + 6)],
                     fill=LEGEND_GOLD)
    draw.rectangle([cx - 10, crown_y + 4, cx + 10, crown_y + 8], fill=LEGEND_GOLD)

    # Floating sparkles
    import random
    rng = random.Random(42)
    for _ in range(8):
        sx = rng.randint(4, w - 4)
        sy = rng.randint(0, h - 10)
        sr = rng.randint(1, 3)
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=LEGEND_GLOW)

    img.save(dst_path)


def process_all():
    for fname in sorted(os.listdir(SRC)):
        if not fname.endswith('.png'):
            continue
        src = os.path.join(SRC, fname)
        make_baby(src, os.path.join(BABY, fname))
        make_legendary(src, os.path.join(LEGENDARY, fname))

    print(f'Generated {len(os.listdir(BABY))} baby sprites')
    print(f'Generated {len(os.listdir(LEGENDARY))} legendary sprites')


if __name__ == '__main__':
    process_all()
