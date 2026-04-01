#!/usr/bin/env python3
"""
Smart11 Carousel Generator
Matches the exact Smart11 brand style:
- Dark background with noise texture
- Gold paint splatter corners
- SMART11 logo centered top
- Bold ALL CAPS white headline with gold accents
- Body text with gold highlights
"""

import json
import os
import sys
import math
import random
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("Run: python -m pip install Pillow")
    sys.exit(1)

# ── Canvas ──────────────────────────────────────────────────────────────
W, H = 1080, 1080

# ── Smart11 Colors ───────────────────────────────────────────────────────
BG          = (13, 13, 13)         # near-black
BG2         = (18, 18, 18)
GOLD        = (240, 165, 20)       # #F0A514 — Smart11 gold
GOLD_DIM    = (240, 165, 20, 180)
ORANGE      = (255, 100, 30)       # orange accent for some highlights
WHITE       = (255, 255, 255)
WHITE_DIM   = (210, 210, 210)
GRAY        = (130, 130, 130)

# ── Font Setup ───────────────────────────────────────────────────────────
FONT_DIRS = [
    Path("C:/Windows/Fonts"),
    Path.home() / ".claude/skills/carousel-maker/fonts",
]

def find_font(names):
    for name in names:
        for d in FONT_DIRS:
            p = d / name
            if p.exists():
                return str(p)
    return None

FONT_BOLD     = find_font(["Impact.ttf", "ariblk.ttf", "arialbd.ttf", "Arial Bold.ttf"])
FONT_REGULAR  = find_font(["arial.ttf", "Arial.ttf"])
FONT_ITALIC   = find_font(["ariali.ttf", "Arial Italic.ttf", "arial.ttf"])

def font(size, style="bold"):
    path = {"bold": FONT_BOLD, "regular": FONT_REGULAR, "italic": FONT_ITALIC}.get(style, FONT_BOLD)
    try:
        if path:
            return ImageFont.truetype(path, size)
    except Exception:
        pass
    return ImageFont.load_default()

# ── Helpers ──────────────────────────────────────────────────────────────

def draw_noise(img, intensity=8):
    """Add subtle noise/grain to image"""
    rng = random.Random(42)
    px = img.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if rng.random() < 0.3:
                n = rng.randint(-intensity, intensity)
                r, g, b, a = px[x, y]
                px[x, y] = (max(0, min(255, r+n)), max(0, min(255, g+n)), max(0, min(255, b+n)), a)

def draw_grid(draw, color=(255,255,255,8)):
    """Subtle dot grid"""
    for y in range(0, H, 40):
        for x in range(0, W, 40):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=color)

def draw_paint_splatter(img, corner="top-left", color=GOLD, seed=1):
    """Draw gold paint splatter in a corner"""
    rng = random.Random(seed)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    if corner == "top-left":
        cx, cy = -30, -30
    elif corner == "top-right":
        cx, cy = W + 30, -30
    elif corner == "bottom-left":
        cx, cy = -30, H + 30
    else:  # bottom-right
        cx, cy = W + 30, H + 30

    # Main blob cluster
    for _ in range(18):
        angle = rng.uniform(0, math.pi * 2)
        dist = rng.uniform(0, 200)
        bx = cx + math.cos(angle) * dist
        by = cy + math.sin(angle) * dist
        size = rng.uniform(15, 80)
        alpha = rng.randint(140, 220)
        c = color + (alpha,) if len(color) == 3 else color
        d.ellipse([bx - size, by - size, bx + size, by + size], fill=c)

    # Drips / streaks
    for _ in range(8):
        angle = rng.uniform(0, math.pi * 2)
        dist = rng.uniform(60, 180)
        bx = cx + math.cos(angle) * dist
        by = cy + math.sin(angle) * dist
        length = rng.uniform(20, 60)
        alpha = rng.randint(100, 180)
        c = color + (alpha,) if len(color) == 3 else color
        d.ellipse([bx - 6, by, bx + 6, by + length], fill=c)

    # Small dots
    for _ in range(25):
        angle = rng.uniform(0, math.pi * 2)
        dist = rng.uniform(80, 280)
        bx = cx + math.cos(angle) * dist
        by = cy + math.sin(angle) * dist
        r = rng.uniform(3, 14)
        alpha = rng.randint(80, 200)
        c = color + (alpha,) if len(color) == 3 else color
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=c)

    # Blur slightly for realism
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1.5))
    img.paste(overlay, mask=overlay)

def make_base(corner1="top-left", corner2="bottom-right"):
    """Create a base canvas with background, noise, grid, splatters"""
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw_noise(img)
    d = ImageDraw.Draw(img, "RGBA")
    draw_grid(d)
    draw_paint_splatter(img, corner1, GOLD, seed=1)
    draw_paint_splatter(img, corner2, GOLD, seed=2)
    return img, d

def draw_logo(d, y=52):
    """Draw SMART11 centered at top"""
    f = font(34, "bold")
    text = "SMART11"
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    # Draw "SMART" in white, "11" in white but italic style
    d.text((x, y), text, font=f, fill=WHITE)

def draw_logo_styled(img, d, y=52):
    """Draw SMART11 with SMART in white and 11 styled"""
    f_bold = font(34, "bold")
    smart_text = "SMART"
    eleven_text = "11"

    bbox_s = d.textbbox((0, 0), smart_text, font=f_bold)
    bbox_e = d.textbbox((0, 0), eleven_text, font=f_bold)
    total_w = (bbox_s[2] - bbox_s[0]) + (bbox_e[2] - bbox_e[0])
    x = (W - total_w) // 2

    d.text((x, y), smart_text, font=f_bold, fill=WHITE)
    d.text((x + bbox_s[2] - bbox_s[0], y), eleven_text, font=f_bold, fill=WHITE)

def text_width(d, text, f):
    bbox = d.textbbox((0, 0), text, font=f)
    return bbox[2] - bbox[0]

def text_height(d, text, f):
    bbox = d.textbbox((0, 0), text, font=f)
    return bbox[3] - bbox[1]

def draw_headline(d, lines_data, start_y, font_size=88, line_spacing=1.1, center=True):
    """
    lines_data: list of lists of (word_text, is_gold) tuples per line
    Draws each line centered, with gold words in GOLD color
    Returns y after last line
    """
    f = font(font_size, "bold")
    y = start_y
    for line_parts in lines_data:
        # Calculate total line width
        total_w = 0
        parts_with_metrics = []
        for item in line_parts:
            word = item[0]
            is_gold = item[1]
            bbox = d.textbbox((0, 0), word, font=f)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            parts_with_metrics.append((word, is_gold, w, h))
            total_w += w

        if center:
            x = (W - total_w) // 2
        else:
            x = 80

        for word, is_gold, w, h in parts_with_metrics:
            color = GOLD if is_gold else WHITE
            d.text((x, y), word, font=f, fill=color)
            x += w

        max_h = max((h for _, _, _, h in parts_with_metrics), default=font_size)
        y += int(max_h * line_spacing)

    return y

def draw_body_text(d, lines_data, start_y, font_size=36, line_spacing=1.5, center=True):
    """
    lines_data: list of lists of (word, is_gold, is_orange) tuples
    """
    f = font(font_size, "bold")
    y = start_y
    for line_parts in lines_data:
        total_w = 0
        parts_with_metrics = []
        for item in line_parts:
            if len(item) == 3:
                word, is_gold, is_orange = item
            else:
                word, is_gold = item
                is_orange = False
            bbox = d.textbbox((0, 0), word, font=f)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            parts_with_metrics.append((word, is_gold, is_orange, w, h))
            total_w += w

        if center:
            x = (W - total_w) // 2
        else:
            x = 80

        for word, is_gold, is_orange, w, h in parts_with_metrics:
            if is_orange:
                color = ORANGE
            elif is_gold:
                color = GOLD
            else:
                color = WHITE_DIM
            d.text((x, y), word, font=f, fill=color)
            x += w

        max_h = max((h for _, _, _, _, h in parts_with_metrics), default=font_size)
        y += int(max_h * line_spacing)

    return y

def parse_accented_text(text, accent_words=None, orange_words=None):
    """
    Parse text into lines of word tuples.
    accent_words: set of words to highlight in gold
    orange_words: set of words to highlight in orange
    Returns list of lines, each line is list of (word, is_gold, is_orange)
    """
    if accent_words is None:
        accent_words = set()
    if orange_words is None:
        orange_words = set()

    lines = text.split("\n")
    result = []
    for line in lines:
        words = line.split(" ")
        parts = []
        for i, word in enumerate(words):
            clean = word.strip(".,!?:")
            is_gold = clean.upper() in {w.upper() for w in accent_words}
            is_orange = clean.upper() in {w.upper() for w in orange_words}
            display = word if i == len(words) - 1 else word + " "
            parts.append((display, is_gold, is_orange))
        result.append(parts)
    return result

def save(img, output_dir, index, name):
    path = Path(output_dir) / f"slide_{index:02d}_{name}.png"
    img.convert("RGB").save(str(path))
    print(f"  [{index}] {name} → {path.name}")
    return str(path)

def add_slide_counter(d, current, total):
    f = font(26, "regular")
    text = f"{current:02d} / {total:02d}"
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    d.text((W - tw - 50, H - 60), text, font=f, fill=GRAY)

# ── Slide Generators ─────────────────────────────────────────────────────

def slide_cover(data, idx, total, output_dir):
    img, d = make_base("top-left", "bottom-right")
    draw_logo_styled(img, d, y=48)

    # Horizontal rule under logo
    d.rectangle([W//2 - 60, 100, W//2 + 60, 103], fill=GOLD)

    title = data.get("title", "")
    accent_words = set(data.get("accent_words", []))
    lines_data = parse_accented_text(title.upper(), accent_words)
    start_y = 160
    end_y = draw_headline(d, lines_data, start_y, font_size=96, line_spacing=1.15)

    # Arrow circle at bottom
    cx, cy = W // 2, H - 120
    r = 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE_DIM, width=2)
    # Arrow
    ax, ay = cx - 14, cy - 14
    d.line([ax, cy, ax + 28, cy], fill=WHITE, width=3)
    d.polygon([ax + 18, cy - 10, ax + 28, cy, ax + 18, cy + 10], fill=WHITE)

    add_slide_counter(d, idx, total)
    return save(img, output_dir, idx, "cover")

def slide_content(data, idx, total, output_dir):
    """Generic content slide: logo + headline + screenshot placeholder + body"""
    img, d = make_base("top-left", "bottom-right")
    draw_logo_styled(img, d, y=40)

    # Headline
    title = data.get("title", "").upper()
    accent_words = set(data.get("accent_words", []))
    lines_data = parse_accented_text(title, accent_words)
    end_y = draw_headline(d, lines_data, 95, font_size=80, line_spacing=1.1)

    # Screenshot area
    ss_top = end_y + 20
    ss_bottom = H - 240
    ss_h = ss_bottom - ss_top
    ss_left = 60
    ss_right = W - 60

    image_path = data.get("image_path")
    if image_path and Path(image_path).exists():
        try:
            shot = Image.open(image_path).convert("RGBA")
            shot.thumbnail((ss_right - ss_left, ss_h), Image.LANCZOS)
            sx = (W - shot.width) // 2
            sy = ss_top + (ss_h - shot.height) // 2
            img.paste(shot, (sx, sy), shot)
        except Exception:
            image_path = None

    if not image_path:
        # Visual placeholder — colored bar with step number
        bar_h = min(ss_h, 320)
        bar_top = ss_top + (ss_h - bar_h) // 2
        d.rectangle([ss_left, bar_top, ss_right, bar_top + bar_h],
                    fill=(25, 25, 25, 255), outline=GOLD + (60,), width=2)
        step_num = data.get("step_number", "")
        if step_num:
            fn = font(120, "bold")
            bbox = d.textbbox((0, 0), str(step_num), font=fn)
            nx = (W - (bbox[2] - bbox[0])) // 2
            ny = bar_top + (bar_h - (bbox[3] - bbox[1])) // 2
            d.text((nx, ny), str(step_num), font=fn, fill=GOLD + (40,))

    # Body text
    body = data.get("body", "").upper()
    orange_words = set(data.get("orange_words", []))
    body_lines = parse_accented_text(body, accent_words, orange_words)
    draw_body_text(d, body_lines, ss_bottom + 18, font_size=32, line_spacing=1.45)

    add_slide_counter(d, idx, total)
    return save(img, output_dir, idx, data.get("slug", f"slide_{idx}"))

def slide_insight(data, idx, total, output_dir):
    img, d = make_base("top-left", "bottom-right")
    draw_logo_styled(img, d, y=48)

    quote = data.get("quote", "").upper()
    source = data.get("source", "").upper()
    accent_words = set(data.get("accent_words", []))

    # Large quote marks
    fq = font(160, "bold")
    d.text((60, 130), "\u201C", font=fq, fill=GOLD + (50,))

    lines_data = parse_accented_text(quote, accent_words)
    end_y = draw_headline(d, lines_data, 240, font_size=72, line_spacing=1.2)

    # Divider
    d.rectangle([W//2 - 40, end_y + 30, W//2 + 40, end_y + 34], fill=GOLD)

    # Source
    f_src = font(30, "regular")
    bbox = d.textbbox((0, 0), source, font=f_src)
    sx = (W - (bbox[2] - bbox[0])) // 2
    d.text((sx, end_y + 52), source, font=f_src, fill=GRAY)

    add_slide_counter(d, idx, total)
    return save(img, output_dir, idx, "insight")

def slide_cta(data, idx, total, output_dir):
    img, d = make_base("top-left", "bottom-right")
    draw_logo_styled(img, d, y=48)

    title = data.get("title", "").upper()
    accent_words = set(data.get("accent_words", []))
    lines_data = parse_accented_text(title, accent_words)
    end_y = draw_headline(d, lines_data, 140, font_size=80, line_spacing=1.15)

    # CTA box
    box_top = end_y + 60
    box_h = 90
    d.rectangle([80, box_top, W - 80, box_top + box_h],
                fill=(30, 30, 30), outline=GOLD + (100,), width=2)

    preview = data.get("preview_label", "")
    fp = font(30, "regular")
    bbox = d.textbbox((0, 0), preview, font=fp)
    px = (W - (bbox[2] - bbox[0])) // 2
    d.text((px, box_top + (box_h - (bbox[3] - bbox[1])) // 2), preview, font=fp, fill=WHITE_DIM)

    # CTA line
    cta_y = box_top + box_h + 50
    cta_text = data.get("cta_text", "")
    cta_highlight = data.get("cta_highlight", "")
    cta_rest = data.get("cta_rest", "")
    full_cta = f"{cta_text} {cta_highlight} {cta_rest}".upper()
    orange_words = {cta_highlight.upper()}

    cta_lines = parse_accented_text(full_cta, set(), orange_words)
    draw_body_text(d, cta_lines, cta_y, font_size=34, line_spacing=1.4)

    add_slide_counter(d, idx, total)
    return save(img, output_dir, idx, "cta")

def slide_follow(data, idx, total, output_dir):
    img, d = make_base("top-left", "bottom-right")
    draw_logo_styled(img, d, y=48)

    lines = data.get("lines", ["VOLG", "VOOR", "MEER"])
    cx, cy = W // 2, H // 2 + 20
    r = 260

    # Circle
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE_DIM, width=3)

    # Lines inside circle
    f_big = font(110, "bold")
    line_h = 120
    start_y = cy - (len(lines) * line_h) // 2

    for i, line in enumerate(lines):
        bbox = d.textbbox((0, 0), line, font=f_big)
        tx = (W - (bbox[2] - bbox[0])) // 2
        color = GOLD if i == 1 else WHITE
        d.text((tx, start_y + i * line_h), line, font=f_big, fill=color)

    add_slide_counter(d, idx, total)
    return save(img, output_dir, idx, "follow")

# ── Main ──────────────────────────────────────────────────────────────────

def generate(data_path, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides = data["slides"]
    total = len(slides)
    topic = data.get("topic", "Carousel")

    print(f"\nGenerating {total} slides: {topic}")
    print("─" * 50)

    for idx, slide in enumerate(slides, 1):
        t = slide.get("type", "content")
        if t == "cover":
            slide_cover(slide, idx, total, output_dir)
        elif t == "insight":
            slide_insight(slide, idx, total, output_dir)
        elif t == "cta":
            slide_cta(slide, idx, total, output_dir)
        elif t == "follow":
            slide_follow(slide, idx, total, output_dir)
        else:
            slide_content(slide, idx, total, output_dir)

    print("─" * 50)
    print(f"Done: {total}/{total} slides → {output_dir}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    generate(args.data, args.output)
