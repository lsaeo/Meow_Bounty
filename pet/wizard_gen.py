"""Wizard cat sprite generator — overlays wizard hat + cape on existing cat sprites."""

import os
from PIL import Image, ImageDraw

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprites')
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wizard_sprites')

HAT_COLOR = (80, 40, 120)     # Purple
HAT_BAND = (200, 170, 50)     # Gold band
CAPE_COLOR = (60, 30, 100)    # Dark purple cape
STAR_COLOR = (255, 230, 100)  # Gold stars


def _add_wizard_hat(draw, w, h):
    """Draw a pointy wizard hat on the top of the sprite."""
    cx = w // 2 - 2
    # Hat body (triangle)
    draw.polygon([(cx - 14, 12), (cx, -12), (cx + 14, 12)], fill=HAT_COLOR)
    # Hat brim
    draw.ellipse([cx - 16, 8, cx + 16, 18], fill=HAT_COLOR)
    # Gold band
    draw.rectangle([cx - 8, 10, cx + 8, 14], fill=HAT_BAND)
    # Star on hat
    star_x, star_y = cx, -2
    r = 3
    for i in range(5):
        a = -1.57 + i * 1.256
        draw.point((star_x + int(r * __import__('math').cos(a)),
                    star_y + int(r * __import__('math').sin(a))), fill=STAR_COLOR)


def _add_cape(draw, w, h):
    """Draw a cape behind/around the body."""
    # Cape shadow at bottom
    draw.polygon([(8, h - 10), (w // 2, h - 2), (w - 8, h - 10)],
                 fill=CAPE_COLOR)
    # Small stars on cape
    for sx, sy in [(16, h - 6), (w - 16, h - 6), (w // 2, h - 14)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=STAR_COLOR)


def process_file(path):
    img = Image.open(path).convert('RGBA')
    w, h = img.size
    draw = ImageDraw.Draw(img)
    _add_wizard_hat(draw, w, h)
    _add_cape(draw, w, h)
    return img


def generate_all():
    os.makedirs(DST, exist_ok=True)
    for fname in os.listdir(SRC):
        if fname.endswith('.png'):
            src_path = os.path.join(SRC, fname)
            img = process_file(src_path)
            dst_path = os.path.join(DST, fname)
            img.save(dst_path)
            print(f'  Generated: {fname}')

    # Copy original angry as-is
    angry_src = os.path.join(SRC, 'angry.png')
    angry_dst = os.path.join(DST, 'angry.png')
    if os.path.exists(angry_src):
        Image.open(angry_src).save(angry_dst)
        print(f'  Copied: angry.png')

    print(f'\nAll wizard sprites saved to: {DST}')
    print('To use them, rename sprites/ -> sprites_old/')
    print('then rename wizard_sprites/ -> sprites/')


if __name__ == '__main__':
    generate_all()
