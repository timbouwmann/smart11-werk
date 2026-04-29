#!/usr/bin/env python3
"""
Smart11 Congres Carousel Generator
Generates 5 × 1080x1080px PNG slides for Instagram/LinkedIn.
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────────────────────────

BASE = Path(__file__).parent.parent
FONT_DIR   = BASE / "brand_assets" / "font"
PHOTO_DIR  = BASE / "brand_assets" / "foto's"
LOGO_DIR   = BASE / "brand_assets" / "logo"
OUTPUT_DIR = BASE / "html_pages" / "congres_carousel"

# ── Brand Colors ───────────────────────────────────────────────────────────────

BG       = (14,  14,  14)        # #0E0E0E
GOLD     = (220, 150,  0)        # #DC9600
GOLD_DIM = (220, 150,  0, 80)
WHITE    = (255, 255, 255)
WHITE_DIM= (200, 200, 200)
GRAY     = (120, 120, 120)

W, H = 1080, 1080
PAD  = 80

# ── Font Loader ────────────────────────────────────────────────────────────────

def load_font(name: str, size: int) -> ImageFont.ImageFont:
    path = FONT_DIR / name
    if path.exists():
        try:
            return ImageFont.truetype(str(path), size)
        except Exception:
            pass
    return ImageFont.load_default()

def bold(size):   return load_font("Poppins-ExtraBold.ttf", size)
def regular(size): return load_font("Poppins-Regular.ttf", size)

# ── Drawing Helpers ────────────────────────────────────────────────────────────

def text_size(draw, text, fnt):
    bb = draw.textbbox((0, 0), text, font=fnt)
    return bb[2] - bb[0], bb[3] - bb[1]

def wrap_text(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], []
    for word in words:
        test = " ".join(cur + [word])
        if text_size(draw, test, fnt)[0] <= max_w:
            cur.append(word)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [word]
    if cur:
        lines.append(" ".join(cur))
    return lines or [""]

def draw_text_wrapped(draw, text, fnt, x, y, max_w, fill=WHITE, line_gap=12, align="left"):
    lines = wrap_text(draw, text, fnt, max_w)
    _, lh = text_size(draw, "Ag", fnt)
    for line in lines:
        lw, _ = text_size(draw, line, fnt)
        if align == "center":
            ox = x + (max_w - lw) // 2
        else:
            ox = x
        draw.text((ox, y), line, font=fnt, fill=fill)
        y += lh + line_gap
    return y


def load_photo_as_overlay(path: Path, opacity: int = 55) -> Image.Image:
    """Load a photo, convert to grayscale, return as RGBA with given opacity."""
    img = Image.open(path).convert("L")          # grayscale
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    a = a.point(lambda x: opacity)               # reduce opacity
    return Image.merge("RGBA", (r, g, b, a))


def composite_photo(base: Image.Image, photo_path: Path, opacity: int = 55) -> Image.Image:
    """Paste a dark photo overlay onto a solid dark base."""
    overlay = load_photo_as_overlay(photo_path, opacity)
    # Scale to fill 1080×1080 (crop center)
    ow, oh = overlay.size
    scale = max(W / ow, H / oh)
    new_w = int(ow * scale)
    new_h = int(oh * scale)
    overlay = overlay.resize((new_w, new_h), Image.LANCZOS)
    ox = (new_w - W) // 2
    oy = (new_h - H) // 2
    overlay = overlay.crop((ox, oy, ox + W, oy + H))

    # Darken even more with gradient overlay from bottom
    result = base.convert("RGBA")
    result.paste(overlay, (0, 0), overlay)

    # Bottom gradient for text readability
    gradient = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gradient)
    for i in range(H):
        alpha = int(160 * (i / H) ** 2.2)
        gd.line([(0, i), (W, i)], fill=(14, 14, 14, alpha))
    result = Image.alpha_composite(result, gradient)

    return result.convert("RGB")


def gold_line(draw, x1, y, x2, thickness=3):
    draw.rectangle([x1, y, x2, y + thickness], fill=GOLD)


def draw_pill(draw, text, fnt, cx, y, pad_h=14, pad_v=10):
    """Draw a centered gold pill/badge. Returns bottom y."""
    tw, th = text_size(draw, text, fnt)
    pill_w = tw + pad_h * 2
    pill_h = th + pad_v * 2
    x = cx - pill_w // 2
    draw.rounded_rectangle([x, y, x + pill_w, y + pill_h], radius=pill_h // 2, fill=GOLD)
    draw.text((x + pad_h, y + pad_v), text, font=fnt, fill=BG + (255,) if len(BG) == 3 else BG)
    return y + pill_h


def draw_cta_button(draw, text, fnt, cx, y, btn_w=480, btn_h=72):
    """Draw a centered gold CTA button. Returns bottom y."""
    x = cx - btn_w // 2
    draw.rounded_rectangle([x, y, x + btn_w, y + btn_h], radius=8, fill=GOLD)
    tw, th = text_size(draw, text, fnt)
    tx = cx - tw // 2
    ty = y + (btn_h - th) // 2
    draw.text((tx, ty), text, font=fnt, fill=(14, 14, 14))
    return y + btn_h


# ── Slide 1 — Hook ─────────────────────────────────────────────────────────────

def slide_1_hook() -> Image.Image:
    photo_path = PHOTO_DIR / "Smart11_V2-5.jpg"
    base = Image.new("RGB", (W, H), BG)

    if photo_path.exists():
        base = composite_photo(base, photo_path, opacity=60)

    draw = ImageDraw.Draw(base)

    # Ghost date as background typographic element
    ghost_fnt = bold(260)
    ghost_text = "30.09.26"
    gw, gh = text_size(draw, ghost_text, ghost_fnt)
    # Draw ghost date centered but large
    ghost_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ghost_img)
    gd.text(((W - gw) // 2, (H - gh) // 2 - 40), ghost_text, font=ghost_fnt,
            fill=(*GOLD, 22))
    base = base.convert("RGBA")
    base = Image.alpha_composite(base, ghost_img).convert("RGB")
    draw = ImageDraw.Draw(base)

    # Gold accent line top-left
    gold_line(draw, PAD, 72, PAD + 56)

    # Headline
    h_fnt = bold(96)
    headline = "Er verandert iets."
    hw, hh = text_size(draw, headline, h_fnt)
    draw.text((PAD, H - 280), headline, font=h_fnt, fill=WHITE)

    # Sub line
    s_fnt = regular(38)
    sub = "Nederlandse coaches, let op."
    draw.text((PAD, H - 280 + hh + 18), sub, font=s_fnt, fill=WHITE_DIM)

    # Slide number bottom right
    num_fnt = regular(26)
    num = "01 / 05"
    nw, _ = text_size(draw, num, num_fnt)
    draw.text((W - PAD - nw, H - 52), num, font=num_fnt, fill=GRAY)

    return base


# ── Slide 2 — Spanning ─────────────────────────────────────────────────────────

def slide_2_tension() -> Image.Image:
    photo_path = PHOTO_DIR / "Smart11_V2-6.jpg"
    base = Image.new("RGB", (W, H), BG)

    if photo_path.exists():
        base = composite_photo(base, photo_path, opacity=55)

    draw = ImageDraw.Draw(base)

    # Top gold line accent
    gold_line(draw, PAD, 72, PAD + 56)

    cy = 180

    # "100 coaches." — very large
    big_fnt = bold(120)
    draw.text((PAD, cy), "100 coaches.", font=big_fnt, fill=WHITE)
    _, bh = text_size(draw, "100 coaches.", big_fnt)
    cy += bh + 28

    # "Één locatie. Eén vraag:"
    med_fnt = regular(44)
    draw.text((PAD, cy), "Één locatie. Eén vraag:", font=med_fnt, fill=WHITE_DIM)
    _, mh = text_size(draw, "Één", med_fnt)
    cy += mh + 40

    # Gold divider line
    gold_line(draw, PAD, cy, PAD + 200)
    cy += 28

    # Quote in gold bold
    q_fnt = bold(62)
    quote = "Hoe maak jij het verschil?"
    draw_text_wrapped(draw, quote, q_fnt, PAD, cy, W - PAD * 2, fill=GOLD, line_gap=14)

    # Slide number
    num_fnt = regular(26)
    num = "02 / 05"
    nw, _ = text_size(draw, num, num_fnt)
    draw.text((W - PAD - nw, H - 52), num, font=num_fnt, fill=GRAY)

    return base


# ── Slide 3 — Pijn / Belofte ───────────────────────────────────────────────────

def slide_3_promise() -> Image.Image:
    photo_path = PHOTO_DIR / "cursus voetbal coach.jpg"
    base = Image.new("RGB", (W, H), BG)

    if photo_path.exists():
        base = composite_photo(base, photo_path, opacity=55)

    draw = ImageDraw.Draw(base)

    cy = 180

    # Top italic light line
    light_fnt = regular(50)
    draw.text((PAD, cy), "Talent zie je pas...", font=light_fnt, fill=WHITE_DIM)
    _, lh = text_size(draw, "Talent", light_fnt)
    cy += lh + 24

    # Gold divider
    gold_line(draw, PAD, cy, W - PAD)
    cy += 28

    # Main bold statement
    main_fnt = bold(68)
    main = "...als je weet waar je naar kijkt."
    cy = draw_text_wrapped(draw, main, main_fnt, PAD, cy, W - PAD * 2, fill=WHITE, line_gap=12)
    cy += 40

    # Small label line
    label_fnt = regular(36)
    draw.text((PAD, cy), "Wij laten het je zien.", font=label_fnt, fill=GOLD)

    # Slide number
    num_fnt = regular(26)
    num = "03 / 05"
    nw, _ = text_size(draw, num, num_fnt)
    draw.text((W - PAD - nw, H - 52), num, font=num_fnt, fill=GRAY)

    return base


# ── Slide 4 — Hint ─────────────────────────────────────────────────────────────

def slide_4_hint() -> Image.Image:
    base = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(base)

    cy = 200

    # Fragment 1 — "Een dag."
    f1_fnt = bold(110)
    draw.text((PAD, cy), "Een dag.", font=f1_fnt, fill=WHITE)
    _, f1h = text_size(draw, "Een dag.", f1_fnt)
    cy += f1h + 36

    # Gold horizontal line
    gold_line(draw, PAD, cy, W - PAD, thickness=3)
    cy += 36

    # Fragment 2
    f2_fnt = regular(52)
    draw.text((PAD, cy), "Sprekers. Inzichten. Praktijk.", font=f2_fnt, fill=WHITE_DIM)
    _, f2h = text_size(draw, "Sprekers.", f2_fnt)
    cy += f2h + 28

    # Fragment 3 — gold
    f3_fnt = bold(58)
    draw.text((PAD, cy), "Jouw aanpak verandert.", font=f3_fnt, fill=GOLD)
    _, f3h = text_size(draw, "Jouw", f3_fnt)
    cy += f3h + 60

    # Bottom hint small text
    hint_fnt = regular(32)
    hint = "Meer info volgt snel  >"
    draw.text((PAD, cy), hint, font=hint_fnt, fill=GRAY)

    # Decorative dot grid pattern (subtle)
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for x in range(PAD, W - PAD, 42):
        for y_dot in range(820, H - 60, 42):
            dd.ellipse([x - 1, y_dot - 1, x + 1, y_dot + 1], fill=(220, 150, 0, 30))
    base = base.convert("RGBA")
    base = Image.alpha_composite(base, dots).convert("RGB")
    draw = ImageDraw.Draw(base)

    # Slide number
    num_fnt = regular(26)
    num = "04 / 05"
    nw, _ = text_size(draw, num, num_fnt)
    draw.text((W - PAD - nw, H - 52), num, font=num_fnt, fill=GRAY)

    return base


# ── Slide 5 — Reveal + CTA ────────────────────────────────────────────────────

def slide_5_reveal() -> Image.Image:
    base = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(base)

    # Subtle radial glow top-right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(60, 0, -1):
        r = int(500 * i / 60)
        a = int(35 * (1 - (i - 1) / 60))
        gd.ellipse([W - r, -r, W + r, r], fill=(*GOLD, a))
    base = base.convert("RGBA")
    base = Image.alpha_composite(base, glow).convert("RGB")
    draw = ImageDraw.Draw(base)

    cy = 72

    # Logo top-center
    logo_path = LOGO_DIR / "T2024010_SMART11_LOGO_WIT_GEEL_RGB (1).png"
    if logo_path.exists():
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_h = 70
            ratio = logo.width / logo.height
            logo_w = int(logo_h * ratio)
            logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
            lx = (W - logo_w) // 2
            base.paste(logo, (lx, cy), logo)
            draw = ImageDraw.Draw(base)
            cy += logo_h + 44
        except Exception:
            cy += 40

    # Gold line under logo
    gold_line(draw, W // 2 - 60, cy, W // 2 + 60)
    cy += 28

    # "Smart11 Congres" — main headline
    h_fnt = bold(88)
    headline = "Smart11 Congres"
    hw, hh = text_size(draw, headline, h_fnt)
    draw.text(((W - hw) // 2, cy), headline, font=h_fnt, fill=WHITE)
    cy += hh + 14

    # Subtitle
    s_fnt = regular(36)
    sub = "Voetbalintelligentie & Talentontwikkeling"
    sw, sh = text_size(draw, sub, s_fnt)
    draw.text(((W - sw) // 2, cy), sub, font=s_fnt, fill=WHITE_DIM)
    cy += sh + 48

    # Date + location block
    date_fnt = bold(44)
    date = "30 september 2026  \u00b7  PEC Zwolle"
    dw, dh = text_size(draw, date, date_fnt)
    draw.text(((W - dw) // 2, cy), date, font=date_fnt, fill=GOLD)
    cy += dh + 50

    # Gold separator line
    gold_line(draw, PAD * 2, cy, W - PAD * 2)
    cy += 36

    # Super Early Bird pill badge
    badge_fnt = bold(32)
    badge_text = "SUPER EARLY BIRD"
    bw, bh = text_size(draw, badge_text, badge_fnt)
    pill_w = bw + 40
    pill_h = bh + 20
    px = (W - pill_w) // 2
    draw.rounded_rectangle([px, cy, px + pill_w, cy + pill_h], radius=pill_h // 2, fill=GOLD)
    draw.text((px + 20, cy + 10), badge_text, font=badge_fnt, fill=(14, 14, 14))
    cy += pill_h + 20

    # "Beperkt aantal plekken beschikbaar"
    lim_fnt = regular(32)
    lim = "Beperkt aantal plekken beschikbaar"
    lw, lh = text_size(draw, lim, lim_fnt)
    draw.text(((W - lw) // 2, cy), lim, font=lim_fnt, fill=WHITE_DIM)
    cy += lh + 40

    # CTA button
    cta_fnt = bold(40)
    cta = "Claim jouw plek  >"
    btn_w = 500
    btn_h = 76
    bx = (W - btn_w) // 2
    draw.rounded_rectangle([bx, cy, bx + btn_w, cy + btn_h], radius=10, fill=GOLD)
    cw, ch = text_size(draw, cta, cta_fnt)
    draw.text(((W - cw) // 2, cy + (btn_h - ch) // 2), cta, font=cta_fnt, fill=(14, 14, 14))
    cy += btn_h + 20

    # Website URL small
    url_fnt = regular(28)
    url = "smart11.ai/congres"
    uw, _ = text_size(draw, url, url_fnt)
    draw.text(((W - uw) // 2, cy), url, font=url_fnt, fill=GRAY)

    # Slide number
    num_fnt = regular(26)
    num = "05 / 05"
    nw, _ = text_size(draw, num, num_fnt)
    draw.text((W - PAD - nw, H - 52), num, font=num_fnt, fill=GRAY)

    return base


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    slides = [
        ("01_hook",    slide_1_hook),
        ("02_tension", slide_2_tension),
        ("03_promise", slide_3_promise),
        ("04_hint",    slide_4_hint),
        ("05_reveal",  slide_5_reveal),
    ]

    print("\nGenerating Smart11 Congres Carousel")
    print("-" * 40)

    for name, fn in slides:
        path = OUTPUT_DIR / f"slide_{name}.png"
        print(f"  {name}...", end=" ", flush=True)
        try:
            img = fn()
            img.save(str(path), "PNG")
            print(f"OK -> {path}")
        except Exception as e:
            import traceback
            print(f"ERROR: {e}")
            traceback.print_exc()

    print("-" * 40)
    print(f"Done -> {OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
